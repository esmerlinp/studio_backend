from typing import List, Optional
from app import db
from app.models.master_scheme.module_model import Module

def get_modules(active_only: bool = False) -> List[Module]:
    query = Module.query
    if active_only:
        query = query.filter(Module.is_active == True)
    return query.order_by(Module.order.asc(), Module.name.asc()).all()

def get_module_by_id(module_id: int) -> Optional[Module]:
    return Module.query.get(module_id)

def create_module(*, name: str, description: str = None, icon: str = None, order: int = None, is_active: bool = True) -> Module:
    module = Module(name=name, description=description, icon=icon, order=order, is_active=is_active)
    db.session.add(module)
    try:
        db.session.commit()
        return module
    except Exception as e:
        db.session.rollback()
        raise e

def update_module(module_id: int, **kwargs) -> Optional[Module]:
    module = get_module_by_id(module_id)
    if not module:
        return None
    
    for key, value in kwargs.items():
        if hasattr(module, key) and value is not None:
            setattr(module, key, value)
    
    try:
        db.session.commit()
        return module
    except Exception as e:
        db.session.rollback()
        raise e

def delete_module(module_id: int) -> bool:
    module = get_module_by_id(module_id)
    if not module:
        return False
    db.session.delete(module)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
