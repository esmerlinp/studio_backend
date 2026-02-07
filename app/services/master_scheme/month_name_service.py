from typing import List, Optional
from app import db
from app.models.master_scheme.month_name_model import MonthName

def get_month_names() -> List[MonthName]:
    return MonthName.query.order_by(MonthName.month_num.asc()).all()

def get_month_by_id(month_id: int) -> Optional[MonthName]:
    return MonthName.query.get(month_id)

def create_month(*, month_num: int, name: str, short_name: str) -> MonthName:
    month = MonthName(month_num=month_num, name=name, short_name=short_name)
    db.session.add(month)
    try:
        db.session.commit()
        return month
    except Exception as e:
        db.session.rollback()
        raise e

def update_month(month_id: int, **kwargs) -> Optional[MonthName]:
    month = get_month_by_id(month_id)
    if not month:
        return None
    
    for key, value in kwargs.items():
        if hasattr(month, key) and value is not None:
            setattr(month, key, value)
    
    try:
        db.session.commit()
        return month
    except Exception as e:
        db.session.rollback()
        raise e

def delete_month(month_id: int) -> bool:
    month = get_month_by_id(month_id)
    if not month:
        return False
    db.session.delete(month)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
