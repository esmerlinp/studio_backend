from app.extensions import db
from app.models.master_scheme.phone_type_model import PhoneType

def get_phone_types():
    return PhoneType.query.all()

def get_phone_type_by_id(pt_id):
    return PhoneType.query.get(pt_id)

def create_phone_type(data):
    pt = PhoneType(**data)
    db.session.add(pt)
    db.session.commit()
    return pt

def update_phone_type(pt_id, data):
    pt = PhoneType.query.get(pt_id)
    if pt:
        for key, value in data.items():
            setattr(pt, key, value)
        db.session.commit()
    return pt

def delete_phone_type(pt_id):
    pt = PhoneType.query.get(pt_id)
    if pt:
        db.session.delete(pt)
        db.session.commit()
        return True
    return False
