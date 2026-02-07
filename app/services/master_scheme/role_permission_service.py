from app.extensions import db
from app.models.master_scheme.role_permission_model import RolePermission

def get_role_permissions():
    return RolePermission.query.all()

def get_role_permission_by_id(rp_id):
    return RolePermission.query.get(rp_id)

def create_role_permission(data):
    rp = RolePermission(**data)
    db.session.add(rp)
    db.session.commit()
    return rp

def update_role_permission(rp_id, data):
    rp = RolePermission.query.get(rp_id)
    if rp:
        for key, value in data.items():
            setattr(rp, key, value)
        db.session.commit()
    return rp

def delete_role_permission(rp_id):
    rp = RolePermission.query.get(rp_id)
    if rp:
        db.session.delete(rp)
        db.session.commit()
        return True
    return False
