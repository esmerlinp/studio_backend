from typing import List, Optional
from app import db
from app.models.master_scheme.marital_status_model import MaritalStatus

def create_marital_status(*, name: str, is_active: bool = True) -> MaritalStatus:
    status = MaritalStatus(name=name, is_active=is_active)
    try:
        db.session.add(status)
        db.session.commit()
        return status
    except Exception:
        db.session.rollback()
        raise

def get_marital_statuses(active_only: bool = False) -> List[MaritalStatus]:
    query = MaritalStatus.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(MaritalStatus.name.asc()).all()

def get_marital_status_by_id(status_id: int) -> Optional[MaritalStatus]:
    return MaritalStatus.query.get(status_id)

def update_marital_status(status_id: int, *, name: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[MaritalStatus]:
    status = MaritalStatus.query.get(status_id)
    if not status:
        return None
    if name is not None:
        status.name = name
    if is_active is not None:
        status.is_active = is_active
    try:
        db.session.commit()
        return status
    except Exception:
        db.session.rollback()
        raise

def delete_marital_status(status_id: int) -> bool:
    status = MaritalStatus.query.get(status_id)
    if not status:
        return False
    try:
        db.session.delete(status)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
