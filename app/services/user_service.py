
from app.models.user_model import User
from app.models.user_preferences_model import UserPreference
from typing import Optional, List
from werkzeug.security import  generate_password_hash
from ..extensions import db 
from app import audit_log

from datetime import datetime, timezone

ACTION_CREATE = "create"
ACTION_UPDATE = "update"
ACTION_DELETE = "delete"
ACTION_READ   = "read"


def get_user_preferences(user_id) -> Optional[UserPreference]:
    prefs = UserPreference.query.filter_by(userId=user_id).first()
    # TODO: No enviar DEFAULT_PREFERENCES cuando cueli elimine la opcion de agregar preferencias en la base de datos
    DEFAULT_PREFERENCES = {
        "language": "es",
        "theme": "light",
        "hourFormat": "24",
        "timeZone":"America/Santo_Domingo",
        "dateFormat": "DD/MM/YYYY",
        "notifications": {
            "email": True,
            "push": False
        }
    }
    prefs.preferences = DEFAULT_PREFERENCES
    return prefs


def add_default_user_preferences(user_id:int,language="es", theme="light", timezone="America/Santo_Domingo", date_format="DD/MM/YYYY", 
                        receive_not_email = True, 
                        push_notifications = False, 
                        hour_format = "24"):
    DEFAULT_PREFERENCES = {
        "language": language,
        "theme": theme,
        "hourFormat": hour_format,
        "timeZone":timezone,
        "dateFormat": date_format,
        "notifications": {
            "email": receive_not_email,
            "push": push_notifications
        }
    }

    prefs = UserPreference(
        userId=user_id,
        preferences=DEFAULT_PREFERENCES
    )

    db.session.add(prefs)
    db.session.commit()
    
    return prefs
    


def update_user_preference(
    user_id: int,
    language: str | None = None,
    theme: str | None = None,
    timezone_: str | None = None,
    date_format: str | None = None,
    hour_format: str | None = None,
    receive_not_email: bool | None = None,
    push_notifications: bool | None = None,
) -> UserPreference:
    prefs = UserPreference.query.filter_by(userId=user_id).first()

    # Crear si no existe
    if not prefs:
        prefs = add_default_user_preferences(user_id=user_id)


    # Asegurar que preferences sea un dict
    if prefs.preferences is None:
        prefs.preferences = {}

    # Actualizar solo lo que venga
    if language is not None:
        prefs.preferences["language"] = language
    

    if hour_format is not None:
        prefs.preferences["hourFormat"] = hour_format

    if theme is not None:
        prefs.preferences["theme"] = theme

    if timezone_ is not None:
        prefs.preferences["timeZone"] = timezone_

    if date_format is not None:
        prefs.preferences["dateFormat"] = date_format

    if receive_not_email is not None:
        prefs.preferences["notifications"]["email"] = receive_not_email

    if push_notifications is not None:
        prefs.preferences['notifications']["push"] = push_notifications

    prefs.updatedAt = datetime.now(timezone.utc)
    #TODO: No esta actualizando en la base de datos VERIFICAR
    db.session.commit()

    return prefs


def get_user_by_user_name_with_passwd(user_name) -> Optional[User]:
    user = User.query.filter_by(username=user_name).first()
    return user


@audit_log(action=ACTION_UPDATE, resource_type="usuarios",description="Cambio de contraseña")
def change_user_password(user_id:int, new_password:int, sessionId=None) -> Optional[User]:
    password_hashed = generate_password_hash(password=new_password)
    
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return None 
    
    user.password = password_hashed
    db.session.commit()
    
    return user
    

def get_user_by_user_name(user_name) -> Optional[User]:
    user = User.query.filter_by(username=user_name).first()
    return user


def get_user_by_email(email) -> Optional[User]:
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_id(user_id:int) -> Optional[User]:
    user = User.query.filter_by(userId=user_id).first()
    return user
    




def get_all_users() -> List[User]:
    users = User.query.all()        
    return users
    


