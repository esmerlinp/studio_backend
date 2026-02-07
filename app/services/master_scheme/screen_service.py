from app.extensions import db
from app.models.master_scheme.screen_model import Screen

def get_screens():
    return Screen.query.order_by(Screen.order).all()

def get_screen_by_id(screen_id):
    return Screen.query.get(screen_id)

def create_screen(data):
    screen = Screen(**data)
    db.session.add(screen)
    db.session.commit()
    return screen

def update_screen(screen_id, data):
    screen = Screen.query.get(screen_id)
    if screen:
        for key, value in data.items():
            setattr(screen, key, value)
        db.session.commit()
    return screen

def delete_screen(screen_id):
    screen = Screen.query.get(screen_id)
    if screen:
        db.session.delete(screen)
        db.session.commit()
        return True
    return False
