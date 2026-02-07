from app.extensions import db
from app.models.master_scheme.blood_type_model import BloodType

def get_blood_types():
    return BloodType.query.all()

def get_blood_type_by_id(bt_id):
    return BloodType.query.get(bt_id)

def create_blood_type(data):
    bt = BloodType(**data)
    db.session.add(bt)
    db.session.commit()
    return bt

def update_blood_type(bt_id, data):
    bt = BloodType.query.get(bt_id)
    if bt:
        for key, value in data.items():
            setattr(bt, key, value)
        db.session.commit()
    return bt

def delete_blood_type(bt_id):
    bt = BloodType.query.get(bt_id)
    if bt:
        db.session.delete(bt)
        db.session.commit()
        return True
    return False
