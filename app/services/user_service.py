
from app.models.master.user_model import User
from app.models.client.user_preferences_model import UserPreference
from typing import Optional, List
from werkzeug.security import  generate_password_hash
from ..extensions import db 
from app import audit_log
from app.models.client.password_policy_model import PasswordPolicy
from app.services.password_service import validate_password_policy
from datetime import datetime, timezone
from app.utils.responses import success, error
from app.utils.helpers import send_email_template, generate_reset_token
from flask import request
from dotenv import load_dotenv
import os


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


@audit_log(action=ACTION_UPDATE, resource_type="usuarios",description="Change password")
def change_user_password(user_id:int, new_password:int, sessionId=None) -> Optional[User]:
    
    
    policy = PasswordPolicy.query.first()

    if policy:
        is_valid, errors = validate_password_policy(new_password, policy)

        if not is_valid:
            raise ValueError(errors)  # 👈 solo lógica de negocio


    
    password_hashed = generate_password_hash(password=new_password)
    
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return None 
    
    try:
        user.password = password_hashed
        user.lastPasswordChangeDate = datetime.now(timezone.utc)
        db.session.commit()
        
        return user
    except Exception as e:
        db.session.rollback()
        raise e

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
    




def insert_user_onboard(
    *,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    uuid: str,
    password: str,
    photo: Optional[str] = None,
    is_active: bool = True,
    is_confirmed_user: bool = False,
    must_change_password: bool = False,
    send_confirm_email = False,
    default_password = False
) -> User:
    """
    Inserta un usuario en el esquema master
    """
    
    #Valida politicas de la contrasena
    load_dotenv()
    
    if not default_password:
        policy = PasswordPolicy.query.first()

        if policy:
            is_valid, errors = validate_password_policy(password, policy)

            if not is_valid:
                raise ValueError(errors)  # 👈 solo lógica de negocio
    else:
        password = "aosU-18fh-stys-3Get"
        
    u = get_user_by_user_name(user_name=username)    
    if u:
        raise ValueError("Usuario ya existe")
    
    u = get_user_by_email(email=email)
    if u:
        raise ValueError("email ya existe")
    
    
    new_user = User(
        username=username,
        firstName=first_name,
        lastName=last_name,
        email=email,
        uuid=uuid,
        photo=photo,
        isActive=is_active,
        isConfirmedUser=is_confirmed_user,
        mustChangePassword=must_change_password,
        loginAttempts=0,
        isBlocked=False,
        blockedDate=None,
        lastLoginDate=None,
        recoveryToken=None,
        tokenExpirationDate=None,
        lastPasswordChangeDate=datetime.now(timezone.utc),
        password=generate_password_hash(password),
    )


    db.session.add(new_user)

    
    #Enviar Email de confirmacion.
    user = get_user_by_user_name(user_name=username)
    if send_confirm_email:
        token = generate_reset_token(user.userId)
        confirmation_url = f"{request.host_url}/confirmation-account?token={token}"
        
        send_email_template(subject="Confirmation Account", 
                            to=[email],
                            path_template="emails/es/confirmation_email.html",
                            confirmation_url=confirmation_url, app_name=os.getenv("APP_NAME"), name=user.firstName
                            )
    
    return user




@audit_log(action=ACTION_CREATE, resource_type="usuarios",description="Create an user")
def insert_user(
    *,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    uuid: str,
    password: str,
    photo: Optional[str] = None,
    is_active: bool = True,
    is_confirmed_user: bool = False,
    must_change_password: bool = False,
    commit:bool = True,
    send_confirm_email = False,
    default_password = False
) -> User:
    """
    Inserta un usuario en el esquema master
    """
    
    #Valida politicas de la contrasena
    load_dotenv()
    
    if not default_password:
        policy = PasswordPolicy.query.first()

        if policy:
            is_valid, errors = validate_password_policy(password, policy)

            if not is_valid:
                raise ValueError(errors)  # 👈 solo lógica de negocio
    else:
        password = "aosU-18fh-stys-3Get"
        
    u = get_user_by_user_name(user_name=username)    
    if u:
        raise ValueError("Usuario ya existe")
    
    u = get_user_by_email(email=email)
    if u:
        raise ValueError("email ya existe")
    
    
    new_user = User(
        username=username,
        firstName=first_name,
        lastName=last_name,
        email=email,
        uuid=uuid,
        photo=photo,
        isActive=is_active,
        isConfirmedUser=is_confirmed_user,
        mustChangePassword=must_change_password,
        loginAttempts=0,
        isBlocked=False,
        blockedDate=None,
        lastLoginDate=None,
        recoveryToken=None,
        tokenExpirationDate=None,
        lastPasswordChangeDate=datetime.now(timezone.utc),
        password=generate_password_hash(password),
    )

    try:
        db.session.add(new_user)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        
        #Enviar Email de confirmacion.
        user = get_user_by_user_name(user_name=username)
        if send_confirm_email:
            token = generate_reset_token(user.userId)
            confirmation_url = f"{request.host_url}/confirmation-account?token={token}"
            
            send_email_template(subject="Confirmation Account", 
                                to=[email],
                                path_template="emails/es/confirmation_email.html",
                                confirmation_url=confirmation_url, app_name=os.getenv("APP_NAME"), name=user.firstName
                                )
        
        return user

    except Exception as e:
        if commit:
            db.session.rollback()
        raise e

    



@audit_log(
    action=ACTION_UPDATE,
    resource_type="usuarios",
    description="Update user"
)
def update_user(
    *,
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    photo: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_confirmed_user: Optional[bool] = None,
    must_change_password: Optional[bool] = None,
    password: Optional[str] = None,
) -> User:
    """
    Actualiza un usuario en el esquema master.
    Solo se actualizan los campos enviados.
    """

    user = User.query.filter_by(userId=user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    # ----------------------------------
    # Cambio de contraseña (opcional)
    # ----------------------------------
    if password:
        policy = PasswordPolicy.query.first()
        if policy:
            is_valid, errors = validate_password_policy(password, policy)
            if not is_valid:
                raise ValueError(errors)

        user.password = generate_password_hash(password)
        user.lastPasswordChangeDate = datetime.now(timezone.utc)
        user.mustChangePassword = False

    # ----------------------------------
    # Actualización de campos simples
    # ----------------------------------
    if username is not None:
        user.username = username

    if first_name is not None:
        user.firstName = first_name

    if last_name is not None:
        user.lastName = last_name

    if email is not None:
        user.email = email

    if photo is not None:
        user.photo = photo

    if is_active is not None:
        user.isActive = is_active

    if is_confirmed_user is not None:
        user.isConfirmedUser = is_confirmed_user

    if must_change_password is not None:
        user.mustChangePassword = must_change_password

    try:
        db.session.commit()
        return user

    except Exception as e:
        db.session.rollback()
        raise e
