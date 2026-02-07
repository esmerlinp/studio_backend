from app.extensions import db
from app.models.master_scheme.profession_model import Profession

def get_professions():
    return Profession.query.all()

def get_profession_by_id(profession_id):
    return Profession.query.get(profession_id)

def create_profession(data):
    profession = Profession(**data)
    db.session.add(profession)
    db.session.commit()
    return profession

def update_profession(profession_id, data):
    profession = Profession.query.get(profession_id)
    if profession:
        for key, value in data.items():
            setattr(profession, key, value)
        db.session.commit()
    return profession

def delete_profession(profession_id):
    profession = Profession.query.get(profession_id)
    if profession:
        db.session.delete(profession)
        db.session.commit()
        return True
    return False
