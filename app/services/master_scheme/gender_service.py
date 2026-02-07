from app.extensions import db
from app.models.master_scheme.gender_model import Gender

def get_genders():
    return Gender.query.all()

def get_gender_by_id(gender_id):
    return Gender.query.get(gender_id)

def create_gender(data):
    gender = Gender(**data)
    db.session.add(gender)
    db.session.commit()
    return gender

def update_gender(gender_id, data):
    gender = Gender.query.get(gender_id)
    if gender:
        for key, value in data.items():
            setattr(gender, key, value)
        db.session.commit()
    return gender

def delete_gender(gender_id):
    gender = Gender.query.get(gender_id)
    if gender:
        db.session.delete(gender)
        db.session.commit()
        return True
    return False
