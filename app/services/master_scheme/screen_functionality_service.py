from app.extensions import db
from app.models.master_scheme.screen_functionality_model import ScreenFunctionality

def get_screen_functionalities():
    return ScreenFunctionality.query.all()

def get_screen_functionality_by_id(sf_id):
    return ScreenFunctionality.query.get(sf_id)

def create_screen_functionality(data):
    sf = ScreenFunctionality(**data)
    db.session.add(sf)
    db.session.commit()
    return sf

def update_screen_functionality(sf_id, data):
    sf = ScreenFunctionality.query.get(sf_id)
    if sf:
        for key, value in data.items():
            setattr(sf, key, value)
        db.session.commit()
    return sf

def delete_screen_functionality(sf_id):
    sf = ScreenFunctionality.query.get(sf_id)
    if sf:
        db.session.delete(sf)
        db.session.commit()
        return True
    return False
