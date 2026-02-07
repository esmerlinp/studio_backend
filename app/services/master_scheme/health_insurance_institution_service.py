from typing import List, Optional
from app import db
from app.models.master_scheme.health_insurance_institution_model import HealthInsuranceInstitution

def create_health_insurance_institution(*, name: str, is_active: bool = True) -> HealthInsuranceInstitution:
    inst = HealthInsuranceInstitution(name=name, is_active=is_active)
    try:
        db.session.add(inst)
        db.session.commit()
        return inst
    except Exception:
        db.session.rollback()
        raise

def get_health_insurance_institutions(active_only: bool = False) -> List[HealthInsuranceInstitution]:
    query = HealthInsuranceInstitution.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(HealthInsuranceInstitution.name.asc()).all()

def get_health_insurance_institution_by_id(inst_id: int) -> Optional[HealthInsuranceInstitution]:
    return HealthInsuranceInstitution.query.get(inst_id)

def update_health_insurance_institution(inst_id: int, *, name: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[HealthInsuranceInstitution]:
    inst = HealthInsuranceInstitution.query.get(inst_id)
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

def delete_health_insurance_institution(inst_id: int) -> bool:
    inst = HealthInsuranceInstitution.query.get(inst_id)
    if not inst:
        return False
    try:
        db.session.delete(inst)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
