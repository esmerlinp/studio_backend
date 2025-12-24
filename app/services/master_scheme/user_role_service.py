from typing import List, Optional
from ...extensions import db
from app.models.client_scheme.user_role_model import UserRole

# ========================
# CREATE
# ========================
def assign_role_to_user(user_id: int, role_id: int, commit:bool = True) -> UserRole:
    """
    Asigna un rol a un usuario. Si ya existe la asignación, retorna la existente.
    """
    existing = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
    if existing:
        return existing

    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.session.add(user_role)
    if commit:
        db.session.commit()
    else:
        db.session.flush()
    return user_role

# ========================
# READ
# ========================
def get_roles_by_user(user_id: int) -> List[UserRole]:
    """Retorna todos los roles asignados a un usuario"""
    return UserRole.query.filter_by(user_id=user_id).all()

def get_users_by_role(role_id: int) -> List[UserRole]:
    """Retorna todos los usuarios asignados a un rol"""
    return UserRole.query.filter_by(role_id=role_id).all()

def get_user_role(user_id: int, role_id: int) -> Optional[UserRole]:
    """Retorna la asignación específica de rol a usuario"""
    return UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()

# ========================
# UPDATE
# ========================
def update_user_role(user_role_id: int, new_role_id: int) -> Optional[UserRole]:
    """
    Actualiza el rol de una asignación existente
    """
    user_role = UserRole.query.get(user_role_id)
    if not user_role:
        return None
    user_role.role_id = new_role_id
    db.session.commit()
    return user_role

# ========================
# DELETE
# ========================
def remove_role_from_user(user_id: int, role_id: int) -> bool:
    """
    Elimina una asignación de rol de un usuario.
    Retorna True si se eliminó, False si no existía.
    """
    user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
    if not user_role:
        return False
    db.session.delete(user_role)
    db.session.commit()
    return True
