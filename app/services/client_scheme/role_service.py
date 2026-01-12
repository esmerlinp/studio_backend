from app.models.client_scheme.role_model import Role
from app import db, audit_log
from app.utils.types import ResourceTypes, ActionType
from typing import Optional, List
from sqlalchemy.exc import IntegrityError


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
        raise ValueError("No se pudo eliminar el rol debido a un error interno.", e)

            
        

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
        if 'scodigo' in str(e.orig).lower():
            raise ValueError(f"El código de rol '{code}' ya existe.")
        if 'srol' in str(e.orig).lower():
            raise ValueError(f"El nombre de rol '{name}' ya existe.")
        
        raise ValueError("Error de integridad: Datos duplicados o inválidos.")

    except Exception as e:
        db.session.rollback()
        # Para errores inesperados, mejor loguear el error real y lanzar algo genérico
        raise ValueError("No se pudo crear el rol debido a un error interno.")
    
 

    
