from typing import List, Optional
from app import db
from app.models.master_scheme.functionality_model import Functionality

def create_functionality(*, name: str, description: Optional[str] = None, code: Optional[str] = None, is_active: bool = True) -> Functionality:
    func = Functionality(name=name, description=description, code=code, is_active=is_active)
    try:
        db.session.add(func)
        db.session.commit()
        return func
    except Exception:
        db.session.rollback()
        raise

def get_functionalities(active_only: bool = False) -> List[Functionality]:
    query = Functionality.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Functionality.name.asc()).all()

def get_functionality_by_id(func_id: int) -> Optional[Functionality]:
    return Functionality.query.get(func_id)

def update_functionality(func_id: int, *, name: Optional[str] = None, description: Optional[str] = None, code: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Functionality]:
    func = Functionality.query.get(func_id)
    if not func:
        return None
    if name is not None:
        func.name = name
    if description is not None:
        func.description = description
    if code is not None:
        func.code = code
    if is_active is not None:
        func.is_active = is_active
    try:
        db.session.commit()
        return func
    except Exception:
        db.session.rollback()
        raise

def delete_functionality(func_id: int) -> bool:
    func = Functionality.query.get(func_id)
    if not func:
        return False
    try:
        db.session.delete(func)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
