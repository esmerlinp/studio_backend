from typing import Optional, List
from datetime import date
from app import db
from app.models.master.client_plans_model import ClientPlan
from app.models.master.plans_model import Plan
from app.models.master.price_list_model import PriceList
from dateutil.relativedelta import relativedelta




def assign_plan_to_client_onboard(
    *,
    client_id: int,
    plan_id: int,
    price_list_id: int,
    start_date: date,
    end_date: Optional[date] = None,
) -> ClientPlan:

    # Validar plan
    plan = Plan.query.get(plan_id)
    if not plan or not plan.is_active:
        raise ValueError("Invalid or inactive plan")

    # Validar lista de precios
    price_list = PriceList.query.get(price_list_id)
    if not price_list or not price_list.is_active:
        raise ValueError("Invalid or inactive price list")

    if price_list.plan_id != plan_id:
        raise ValueError("Price list does not belong to the selected plan")


    if plan.code == "TRIAL":
        end_date = start_date + relativedelta(months=6)
        
    # Evitar dos planes activos simultáneos
    active_plan = ClientPlan.query.filter(
        ClientPlan.client_id == client_id,
        ClientPlan.status == "ACTIVE",
        ClientPlan.start_date <= start_date,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= start_date
        )
    ).first()

    if active_plan:
        raise ValueError("Client already has an active plan for this period")

    client_plan = ClientPlan(
        client_id=client_id,
        plan_id=plan_id,
        price_list_id=price_list_id,
        start_date=start_date,
        end_date=end_date,
        status="ACTIVE"
    )


    db.session.add(client_plan)
    return client_plan


def assign_plan_to_client(
    *,
    client_id: int,
    plan_id: int,
    price_list_id: int,
    start_date: date,
    end_date: Optional[date] = None,
    commit: bool = True
) -> ClientPlan:

    # Validar plan
    plan = Plan.query.get(plan_id)
    if not plan or not plan.is_active:
        raise ValueError("Invalid or inactive plan")

    # Validar lista de precios
    price_list = PriceList.query.get(price_list_id)
    if not price_list or not price_list.is_active:
        raise ValueError("Invalid or inactive price list")

    if price_list.plan_id != plan_id:
        raise ValueError("Price list does not belong to the selected plan")


    if plan.code == "TRIAL":
        end_date = start_date + relativedelta(months=6)
        
    # Evitar dos planes activos simultáneos
    active_plan = ClientPlan.query.filter(
        ClientPlan.client_id == client_id,
        ClientPlan.status == "ACTIVE",
        ClientPlan.start_date <= start_date,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= start_date
        )
    ).first()

    if active_plan:
        raise ValueError("Client already has an active plan for this period")

    client_plan = ClientPlan(
        client_id=client_id,
        plan_id=plan_id,
        price_list_id=price_list_id,
        start_date=start_date,
        end_date=end_date,
        status="ACTIVE"
    )

    try:
        db.session.add(client_plan)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return client_plan
    except Exception as e:
        if commit:
            db.session.rollback()
        raise e



def get_active_client_plan(client_id: int) -> Optional[ClientPlan]:
    today = date.today()

    return ClientPlan.query.filter(
        ClientPlan.client_id == client_id,
        ClientPlan.status == "ACTIVE",
        ClientPlan.start_date <= today,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= today)
    ).order_by(ClientPlan.start_date.desc()).first()



def get_client_plan_history(client_id: int) -> List[ClientPlan]:
    return ClientPlan.query.filter_by(
        client_id=client_id
    ).order_by(ClientPlan.start_date.desc()).all()



def update_client_plan(
    client_plan_id: int,
    *,
    end_date: Optional[date] = None,
    status: Optional[str] = None
) -> Optional[ClientPlan]:

    client_plan = ClientPlan.query.get(client_plan_id)
    if not client_plan:
        return None

    if end_date is not None:
        client_plan.end_date = end_date

    if status is not None:
        if status not in ("ACTIVE", "SUSPENDED", "CANCELLED"):
            raise ValueError("Invalid status")
        client_plan.status = status

    try:
        db.session.commit()
        return client_plan
    except Exception:
        db.session.rollback()
        raise



def change_client_plan(
    *,
    client_id: int,
    new_plan_id: int,
    new_price_list_id: int,
    change_date: date
) -> ClientPlan:

    current_plan = get_active_client_plan(client_id)
    if not current_plan:
        raise ValueError("Client has no active plan")

    # Finalizar plan actual
    current_plan.end_date = change_date
    current_plan.status = "CANCELLED"

    try:
        db.session.flush()

        # Asignar nuevo plan
        return assign_plan_to_client(
            client_id=client_id,
            plan_id=new_plan_id,
            price_list_id=new_price_list_id,
            start_date=change_date
        )

    except Exception:
        db.session.rollback()
        raise


def cancel_client_plan(
    client_plan_id: int,
    cancel_date: Optional[date] = None
) -> bool:

    client_plan = ClientPlan.query.get(client_plan_id)
    if not client_plan:
        return False

    client_plan.status = "CANCELLED"
    client_plan.end_date = cancel_date or date.today()

    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
