from typing import Optional, List
from datetime import date
from app import db
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.plans_model import Plan
from app.models.master_scheme.price_list_model import PriceList
from dateutil.relativedelta import relativedelta
from app import audit_log
from app.utils.types import ActionType, ResourceTypes, states
from flask import g


def assign_plan_to_client_onboard(
    *,
    client_id: int,
    plan_id: int,
    price_list_id: int,
    start_date: date,
    end_date: Optional[date] = None,
    status=states.ACTIVE
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
        ClientPlan.status == states.ACTIVE,
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
        status=status
    )


    db.session.add(client_plan)
    return client_plan



@audit_log(action=ActionType.CREATE, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           description="Asociar plan a cliente")
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

    g.audit_resource_id = plan.id
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
        ClientPlan.status == states.ACTIVE,
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
        g.audit_new_values = client_plan.to_dict()
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return client_plan
    except Exception as e:
        if commit:
            db.session.rollback()
        raise e



@audit_log(action=ActionType.READ, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="client_id", 
           description="Consultar plan activo de  cliente")
def get_active_client_plan(client_id: int) -> Optional[ClientPlan]:
    today = date.today()

    client_plan = ClientPlan.query.filter(
        ClientPlan.client_id == client_id,
        ClientPlan.status == states.ACTIVE,
        ClientPlan.start_date <= today,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= today)
    ).order_by(ClientPlan.start_date.desc()).first()

    g.audit_resource_id = client_plan.id
    return client_plan


@audit_log(action=ActionType.READ, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="id", 
           description="Consultar plan")
def get_active_plan(id: int) -> Optional[ClientPlan]:
    today = date.today()

    client_plan = ClientPlan.query.filter(
        ClientPlan.id == id,
        ClientPlan.status == states.ACTIVE,
        ClientPlan.start_date <= today,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= today)
    ).order_by(ClientPlan.start_date.desc()).first()
    
    g.audit_resource_id = client_plan.id
    return client_plan
    
    
@audit_log(action=ActionType.READ, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="id", 
           description="Consultar plan")
def get_active_pending(id: int) -> Optional[ClientPlan]:
    today = date.today()

    return ClientPlan.query.filter(
        ClientPlan.id == id,
        ClientPlan.status == states.PENDING_PAYMENT,
        ClientPlan.start_date <= today,
        db.or_(
            ClientPlan.end_date.is_(None),
            ClientPlan.end_date >= today)
    ).order_by(ClientPlan.start_date.desc()).first()
    

@audit_log(action=ActionType.READ, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="client_id", 
           description="Consultar historico de planes del cliente")
def get_client_plan_history(client_id: int) -> List[ClientPlan]:
    client_plan = ClientPlan.query.filter_by(
        client_id=client_id
    ).order_by(ClientPlan.start_date.desc()).all()
    
    g.audit_resource_id = client_plan.id
    return client_plan

@audit_log(action=ActionType.UPDATE, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="client_plan_id", 
           description="Actualizar plan")
def update_client_plan(
    client_plan_id: int,
    *,
    end_date: Optional[date] = None,
    status: Optional[str] = None
) -> Optional[ClientPlan]:

    client_plan = ClientPlan.query.get(client_plan_id)
    if not client_plan:
        return None
    
    g.audit_resource_id = client_plan.id
    g.audit_old_values = client_plan.to_dict()
    if end_date is not None:
        client_plan.end_date = end_date

    if status is not None:
        if status not in (states.ACTIVE, states.SUSPENDED, states.CANCELLED):
            raise ValueError("Invalid status")
        client_plan.status = status

    try:
        g.audit_new_values = client_plan.to_dict()

        db.session.commit()
        return client_plan
    except Exception:
        db.session.rollback()
        raise


@audit_log(action=ActionType.UPDATE, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="client_id", 
           description="Cambiar plan de cliente")
def change_client_plan(
    *,
    client_id: int,
    new_plan_id: int,
    new_price_list_id: int,
    change_date: date = date.today()
) -> ClientPlan:

    current_plan = get_active_client_plan(client_id)
    if not current_plan:
        raise ValueError("Client has no active plan")

    g.audit_resource_id = current_plan.id
    g.audit_old_values = current_plan.to_dict()

    # Finalizar plan actual
    current_plan.end_date = change_date
    current_plan.status = states.CANCELLED

    try:
        db.session.flush()

        # Asignar nuevo plan
        new_plan = assign_plan_to_client(
            client_id=client_id,
            plan_id=new_plan_id,
            price_list_id=new_price_list_id,
            start_date=change_date
        )
        
        g.audit_new_values = new_plan.to_dict()

        return new_plan

    except Exception as e:
        db.session.rollback()
        raise



@audit_log(action=ActionType.UPDATE, 
           resource_type=ResourceTypes.CLIENT_PLAN,
           resource_id_arg="client_plan_id", 
           description="Cancelar plan")
def cancel_client_plan(
    client_plan_id: int,
    cancel_date: Optional[date] = None
) -> bool:

    client_plan = ClientPlan.query.get(client_plan_id)
    if not client_plan:
        return False
    g.audit_resource_id = client_plan.id
    g.audit_old_values = client_plan.to_dict()
    
    client_plan.status = states.CANCELLED
    client_plan.end_date = cancel_date or date.today()

    try:
        g.audit_new_values = client_plan.to_dict()
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
