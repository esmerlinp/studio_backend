from typing import List, Optional
from app import db
from app.models.master_scheme.medical_institution_model import MedicalInstitution

def create_medical_institution(*, name: str, is_active: bool = True) -> MedicalInstitution:
    inst = MedicalInstitution(name=name, is_active=is_active)
    try:
        db.session.add(inst)
        db.session.commit()
        return inst
    except Exception:
        db.session.rollback()
        raise

def get_medical_institutions(active_only: bool = False) -> List[MedicalInstitution]:
    query = MedicalInstitution.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(MedicalInstitution.name.asc()).all()

def get_medical_institution_by_id(inst_id: int) -> Optional[MedicalInstitution]:
    return MedicalInstitution.query.get(inst_id)

def update_medical_institution(inst_id: int, *, name: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[MedicalInstitution]:
    inst = MedicalInstitution.query.get(inst_id)
    if not inst:
        return None
    if name is not None:
        inst.name = name
    if is_active is not None:
        inst.is_active = is_active
    try:
        db.session.commit()
        return inst
    except Exception:
        db.session.rollback()
        raise

def delete_medical_institution(inst_id: int) -> bool:
    inst = MedicalInstitution.query.get(inst_id)
    if not inst:
        return False
    try:
        db.session.delete(inst)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
