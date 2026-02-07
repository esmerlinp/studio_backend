from typing import List, Optional
from app import db
from app.models.master_scheme.other_school_model import OtherSchool

def get_other_schools(active_only: bool = False) -> List[OtherSchool]:
    query = OtherSchool.query
    if active_only:
        query = query.filter(OtherSchool.is_active == True)
    return query.order_by(OtherSchool.name.asc()).all()

def get_other_school_by_id(school_id: int) -> Optional[OtherSchool]:
    return OtherSchool.query.get(school_id)

def create_other_school(*, id: int, name: str, is_active: bool = True) -> OtherSchool:
    school = OtherSchool(id=id, name=name, is_active=is_active)
    db.session.add(school)
    try:
        db.session.commit()
        return school
    except Exception as e:
        db.session.rollback()
        raise e

def update_other_school(school_id: int, **kwargs) -> Optional[OtherSchool]:
    school = get_other_school_by_id(school_id)
    if not school:
        return None
    
    for key, value in kwargs.items():
        if hasattr(school, key) and value is not None:
            setattr(school, key, value)
    
    try:
        db.session.commit()
        return school
    except Exception as e:
        db.session.rollback()
        raise e

def delete_other_school(school_id: int) -> bool:
    school = get_other_school_by_id(school_id)
    if not school:
        return False
    db.session.delete(school)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
