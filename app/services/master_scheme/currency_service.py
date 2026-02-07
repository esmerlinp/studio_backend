from typing import List, Optional
from app import db
from app.models.master_scheme.currency_model import Currency

def get_currencies(active_only: bool = False) -> List[Currency]:
    query = Currency.query
    if active_only:
        query = query.filter(Currency.is_active == True)
    return query.order_by(Currency.name.asc()).all()

def get_currency_by_id(currency_id: int) -> Optional[Currency]:
    return Currency.query.get(currency_id)

def create_currency(*, name: str, iso_code: str, is_active: bool = True) -> Currency:
    currency = Currency(name=name, iso_code=iso_code, is_active=is_active)
    db.session.add(currency)
    try:
        db.session.commit()
        return currency
    except Exception as e:
        db.session.rollback()
        raise e

def update_currency(currency_id: int, **kwargs) -> Optional[Currency]:
    currency = get_currency_by_id(currency_id)
    if not currency:
        return None
    
    for key, value in kwargs.items():
        if hasattr(currency, key) and value is not None:
            setattr(currency, key, value)
    
    try:
        db.session.commit()
        return currency
    except Exception as e:
        db.session.rollback()
        raise e

def delete_currency(currency_id: int) -> bool:
    currency = get_currency_by_id(currency_id)
    if not currency:
        return False
    db.session.delete(currency)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
