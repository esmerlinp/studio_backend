from app.models.client_scheme.role_model import Role
from app import db, audit_log
from app.utils.types import ResourceTypes, ActionType
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from app.utils import i18n  # Importar el módulo de idiomas

@audit_log(action=ActionType.READ, resource_type=ResourceTypes.ROLE)
def get_all_roles() -> Optional[list[Role]]:
    roles = db.session.query(Role)\
        .filter(Role.is_active==True)\
        .all()
    return roles


def delete_role(role_id) -> int:
    role = db.session.query(Role).filter(Role.id == role_id).first()
    if not role:
        return 0
    try:
        db.session.delete(role)
        db.session.commit()
        return role.id
    except Exception as e:
        db.session.rollback()
        raise ValueError(i18n._("error.role.delete_failed"), e)

            
        

@audit_log(action=ActionType.CREATE, resource_type=ResourceTypes.ROLE)
def create_role(name, code, description) -> Role:
    try:
        role = Role(name=name, code=code, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    except IntegrityError as e:
        db.session.rollback()
        # Verificamos si el error es por el código único
        error_str = str(e.orig).lower()
        if 'scodigo' in str(e.orig).lower():
            raise ValueError(i18n._("error.role.code_exists") % code)
        if 'srol' in str(e.orig).lower():
            raise ValueError(i18n._("error.role.name_exists") % name)
        
        raise ValueError(i18n._("error.role.integrity_error"))

    except Exception as e:
        db.session.rollback()
        # Para errores inesperados, mejor loguear el error real y lanzar algo genérico
        raise ValueError(i18n._("error.role.internal_error"))
    
 

    
