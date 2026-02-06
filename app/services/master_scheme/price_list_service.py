from datetime import time
from typing import List, Optional
from app import db
from app.models.master_scheme.price_list_model import PriceList
from app.utils.helpers import format_datetime_user
from app.utils.types import Roles as r
from app.utils import i18n
import json

def create_price_list(
    *,
    plan_id: int,
    billing_cycle: str,
    price: float,
    currency: str = "USD",
    price_per_user: bool = False,
    min_users: int = 1,
    valid_from: str,
    valid_to: Optional[str] = None,
    features_config: dict = {},
    is_trial: bool = False,
    trial_days: int = 0
) -> PriceList:
    # 1. Validar que no exista cruce de fechas para el mismo plan y ciclo (opcional pero recomendado)
    price_list = PriceList(
        plan_id=plan_id,
        billing_cycle=billing_cycle,
        price=price,
        currency=currency,
        price_per_user=price_per_user,
        min_users=min_users,
        valid_from=valid_from,
        valid_to=valid_to,
        features_config=features_config,
        is_trial=is_trial,
        trial_days=trial_days
    )

    try:
        db.session.add(price_list)
        db.session.commit()
        return price_list
    except Exception:
        db.session.rollback()
        raise

def get_price_lists(plan_id: int = None) -> List[PriceList]:
    query = PriceList.query
    if plan_id:
        query = query.filter_by(plan_id=plan_id)
    return query.order_by(PriceList.id.desc()).all()


def update_price_list_service(price_id: int, data: dict) -> PriceList:
    price_list = PriceList.query.get(price_id)
    if not price_list:
        raise ValueError(i18n._("error.price_list.not_found"))
    
    if 'price' in data: price_list.price = data['price']
    if 'billing_cycle' in data: price_list.billing_cycle = data['billing_cycle']
    if 'is_active' in data: price_list.is_active = data['is_active']
    if 'price_per_user' in data: price_list.price_per_user = data['price_per_user']
    if 'valid_to' in data: price_list.valid_to = data['valid_to']
    if 'is_trial' in data: price_list.is_trial = data['is_trial']
    if 'trial_days' in data: price_list.trial_days = data['trial_days']
    
    db.session.commit()
    return price_list
