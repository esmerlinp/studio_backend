from typing import List, Optional
from datetime import date
from app import db
from app.models.master_scheme.price_list_model import PriceList
from app.models.master_scheme.plans_model import Plan


def create_price_list(
    *,
    plan_id: int,
    billing_cycle: str,
    price: float,
    currency: str = "USD",
    price_per_user: bool = True,
    min_users: int = 1,
    valid_from: date,
    valid_to: Optional[date] = None,
    features_config: dict ={}
) -> PriceList:

    # Validar plan
    plan = Plan.query.get(plan_id)
    if not plan:
        raise ValueError("Plan not found")

    # Evitar solapamiento de precios activos
    overlapping = PriceList.query.filter(
        PriceList.plan_id == plan_id,
        PriceList.billing_cycle == billing_cycle,
        PriceList.is_active.is_(True),
        PriceList.valid_from <= valid_from,
        db.or_(
            PriceList.valid_to.is_(None),
            PriceList.valid_to >= valid_from
        )
    ).first()

    if overlapping:
        raise ValueError("There is already an active price list for this plan and billing cycle")

    price_list = PriceList(
        plan_id=plan_id,
        billing_cycle=billing_cycle,
        price=price,
        currency=currency,
        price_per_user=price_per_user,
        min_users=min_users,
        valid_from=valid_from,
        valid_to=valid_to,
        is_active=True,
        features_config=features_config
    )

    try:
        db.session.add(price_list)
        db.session.commit()
        return price_list
    except Exception:
        db.session.rollback()
        raise



def get_price_lists(
    *,
    plan_id: Optional[int] = None,
    active_only: bool = True
) -> List[PriceList]:

    query = PriceList.query

    if plan_id:
        query = query.filter_by(plan_id=plan_id)

    if active_only:
        query = query.filter_by(is_active=True)

    return query.order_by(PriceList.created_at.desc()).all()



def get_current_price(
    plan_id: int,
    billing_cycle: str,
    reference_date: Optional[date] = None
) -> Optional[PriceList]:

    reference_date = reference_date or date.today()

    return PriceList.query.filter(
        PriceList.plan_id == plan_id,
        PriceList.billing_cycle == billing_cycle,
        PriceList.is_active.is_(True),
        PriceList.valid_from <= reference_date,
        db.or_(
            PriceList.valid_to.is_(None),
            PriceList.valid_to >= reference_date
        )
    ).order_by(PriceList.valid_from.desc()).first()



def update_price_list(
    price_list_id: int,
    *,
    price: Optional[float] = None,
    currency: Optional[str] = None,
    price_per_user: Optional[bool] = None,
    min_users: Optional[int] = None,
    valid_to: Optional[date] = None,
    is_active: Optional[bool] = None,
    features_config: Optional[dict] = None
) -> Optional[PriceList]:

    price_list = PriceList.query.get(price_list_id)
    if not price_list:
        return None

    if price is not None:
        price_list.price = price
    if currency is not None:
        price_list.currency = currency
    if price_per_user is not None:
        price_list.price_per_user = price_per_user
    if min_users is not None:
        price_list.min_users = min_users
    if valid_to is not None:
        price_list.valid_to = valid_to
    if is_active is not None:
        price_list.is_active = is_active
    if features_config is not None:
        price_list.features_config = features_config

    try:
        db.session.commit()
        return price_list
    except Exception:
        db.session.rollback()
        raise




def deactivate_price_list(price_list_id: int) -> bool:
    price_list = PriceList.query.get(price_list_id)
    if not price_list:
        return False

    price_list.is_active = False

    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
