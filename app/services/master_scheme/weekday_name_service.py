from typing import List, Optional
from app import db
from app.models.master_scheme.weekday_name_model import WeekdayName

def get_weekday_names() -> List[WeekdayName]:
    return WeekdayName.query.order_by(WeekdayName.weekday_num.asc()).all()

def get_weekday_by_id(weekday_id: int) -> Optional[WeekdayName]:
    return WeekdayName.query.get(weekday_id)

def create_weekday(*, weekday_num: int, name: str, short_name: str) -> WeekdayName:
    weekday = WeekdayName(weekday_num=weekday_num, name=name, short_name=short_name)
    db.session.add(weekday)
    try:
        db.session.commit()
        return weekday
    except Exception as e:
        db.session.rollback()
        raise e

def update_weekday(weekday_id: int, **kwargs) -> Optional[WeekdayName]:
    weekday = get_weekday_by_id(weekday_id)
    if not weekday:
        return None
    
    for key, value in kwargs.items():
        if hasattr(weekday, key) and value is not None:
            setattr(weekday, key, value)
    
    try:
        db.session.commit()
        return weekday
    except Exception as e:
        db.session.rollback()
        raise e

def delete_weekday(weekday_id: int) -> bool:
    weekday = get_weekday_by_id(weekday_id)
    if not weekday:
        return False
    db.session.delete(weekday)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
