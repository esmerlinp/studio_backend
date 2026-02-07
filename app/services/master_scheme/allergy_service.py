from typing import List, Optional
from app import db
from app.models.master_scheme.allergy_model import Allergy
from app.utils import i18n

def create_allergy(*, id: int, name: str, is_active: bool = True) -> Allergy:
    if Allergy.query.get(id):
        raise ValueError(i18n._("error.allergy_id_already_exists"))

    allergy = Allergy(id=id, name=name, is_active=is_active)
    
    try:
        db.session.add(allergy)
        db.session.commit()
        return allergy
    except Exception:
        db.session.rollback()
        raise

def get_allergies(active_only: bool = False) -> List[Allergy]:
    query = Allergy.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Allergy.id.asc()).all()

def get_allergy_by_id(allergy_id: int) -> Optional[Allergy]:
    return Allergy.query.get(allergy_id)

def update_allergy(allergy_id: int, *, name: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Allergy]:
    allergy = Allergy.query.get(allergy_id)
    if not allergy:
        return None

    if name is not None:
        allergy.name = name
    if is_active is not None:
        allergy.is_active = is_active

    try:
        db.session.commit()
        return allergy
    except Exception:
        db.session.rollback()
        raise

def deactivate_allergy(allergy_id: int) -> bool:
    allergy = Allergy.query.get(allergy_id)
    if not allergy:
        return False
    
    allergy.is_active = False
    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise

def delete_allergy(allergy_id: int) -> bool:
    allergy = Allergy.query.get(allergy_id)
    if not allergy:
        return False
    
    try:
        db.session.delete(allergy)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
