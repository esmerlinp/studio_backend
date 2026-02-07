from app.extensions import db
from app.models.master_scheme.roles_model import Role

def get_roles():
    return Role.query.all()

def get_role_by_id(role_id):
    return Role.query.get(role_id)

def create_role(data):
    role = Role(**data)
    db.session.add(role)
    db.session.commit()
    return role

def update_role(role_id, data):
    role = Role.query.get(role_id)
    if role:
        for key, value in data.items():
            setattr(role, key, value)
        db.session.commit()
    return role

def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return True
    return False
