from typing import List, Optional
from app import db
from app.models.master_scheme.function_model import Function

def create_function(*, name: str, description: str, example: str, is_active: bool = True) -> Function:
    func = Function(name=name, description=description, example=example, is_active=is_active)
    try:
        db.session.add(func)
        db.session.commit()
        return func
    except Exception:
        db.session.rollback()
        raise

def get_functions(active_only: bool = False) -> List[Function]:
    query = Function.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Function.name.asc()).all()

def get_function_by_id(func_id: int) -> Optional[Function]:
    return Function.query.get(func_id)

def update_function(func_id: int, *, name: Optional[str] = None, description: Optional[str] = None, example: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Function]:
    func = Function.query.get(func_id)
    if not func:
        return None
    if name is not None:
        func.name = name
    if description is not None:
        func.description = description
    if example is not None:
        func.example = example
    if is_active is not None:
        func.is_active = is_active
    try:
        db.session.commit()
        return func
    except Exception:
        db.session.rollback()
        raise

def delete_function(func_id: int) -> bool:
    func = Function.query.get(func_id)
    if not func:
        return False
    try:
        db.session.delete(func)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
