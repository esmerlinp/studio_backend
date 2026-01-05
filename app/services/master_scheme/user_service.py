
from app.models.master_scheme.user_model import User
from app.models.master_scheme.user_preferences_model import UserPreference
from typing import Optional, List
from werkzeug.security import  generate_password_hash
from ...extensions import db 
from app import audit_log
from app.models.client_scheme.password_policy_model import PasswordPolicy
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.services.master_scheme.password_service import validate_password_policy
from app.services.master_scheme.user_client_service import assign_user_to_client
from datetime import datetime, timezone
from app.utils.responses import success, error
from app.utils.helpers import send_email_template, generate_reset_token, send_confirmation_account_email
from flask import request, g
from dotenv import load_dotenv
import os
from uuid import uuid4





def get_user_scheme(user_id:int)-> Optional[str]:
    relacion = UsuarioCliente.query.filter_by(user_id=user_id).first()
    if relacion:
        cliente = Client.query.filter_by(uuid=relacion.client_uuid).first()
    
        if cliente:
            return cliente.schemaName
        
    return None
    
def get_user_preferences(user_id) -> Optional[UserPreference]:
    prefs = UserPreference.query.filter_by(userId=user_id).first()
    return prefs

def add_default_user_preferences_onboard(user_id:int,language="es", theme="light", timezone="America/Santo_Domingo", date_format="DD/MM/YYYY", 
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


    return prefs

def add_default_user_preferences(user_id:int,language="es", theme="light", timezone="America/Santo_Domingo", date_format="DD/MM/YYYY", 
                        receive_not_email = True, 
                        push_notifications = False, 
                        hour_format = "24"):
    default_data = {
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
        preferences=default_data
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
        user.mustChangePassword = False
        user.isConfirmedUser = True
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
    
def get_client_users(user_id) -> List[User]:
    cliente_del_usuario = UsuarioCliente.query.filter_by(user_id=user_id).first()
    
    users = db.session.query(User)\
        .join(UsuarioCliente, User.userId==UsuarioCliente.user_id)\
        .filter(UsuarioCliente.client_uuid == cliente_del_usuario.client_uuid)\
        .all()
        
    return users
    
def insert_user_onboard(
    *,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    uuid: str,
    password: str="aosU-18fh-stys-3Get",
    photo: Optional[str] = None,
    is_active: bool = False,
    is_confirmed_user: bool = False,
    must_change_password: bool = True,
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
        rol="OWNER"
    )


    db.session.add(new_user)

    
    #Enviar Email de confirmacion.
    user = get_user_by_user_name(user_name=username)
    add_default_user_preferences_onboard(user.userId)
    if send_confirm_email:
        token = generate_reset_token(user.userId)
        confirmation_url = f"{request.host_url}/confirmation-account?token={token}"
        
        send_email_template(subject="Confirmation Account", 
                            to=[email],
                            path_template="emails/es/confirmation_email.html",
                            confirmation_url=confirmation_url, app_name=os.getenv("APP_NAME"), name=user.firstName
                            )
    
    return user

def insert_user(
    *,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    client_uuid:str,
    password: str = "aosU-18fh-stys-3Get*",
    photo: Optional[str] = None,
    is_active: bool = False,
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
    uuid = str(uuid4())
    
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
        if not u.isActive and not u.isConfirmedUser:
            send_confirmation_account_email(user_id=u.userId, user_name=u.username, email=u.email)
        raise ValueError("Usuario ya existe")
    
    u = get_user_by_email(email=email)
    if u:
        if not u.isActive and not u.isConfirmedUser:
            send_confirmation_account_email(user_id=u.userId, user_name=u.username, email=u.email)
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
        rol="USER"
    )

    try:
        
        
        db.session.add(new_user)
        db.session.flush()
        
        g.audit_new_values = new_user.to_dict()
        #Relacionar el usuario al cliente.
        assign_user_to_client(user_id=new_user.userId, client_uuid=client_uuid, commit=False)
        
        db.session.commit()

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

    g.audit_old_values = user.to_dict()
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
        
        
        g.audit_new_values = user.to_dict()
        db.session.commit()
        return user

    except Exception as e:
        db.session.rollback()
        raise e


def deactivate_user(user_id, admin_user_id):
    # 1. Obtener las relaciones
    cliente_usuario_a_inactivar = UsuarioCliente.query.filter_by(user_id=user_id).first()
    cliente_del_usuario_administrador = UsuarioCliente.query.filter_by(user_id=admin_user_id).first()

    # 2. Validar que ambos existan (No sean None)
    if not cliente_usuario_a_inactivar or not cliente_del_usuario_administrador:
        # Si falta alguno, es un error de "No encontrado" o "Sesión inválida"
        raise ValueError("No se pudo verificar la relación del usuario con la institución.")

    # 3. Validar que pertenezcan al mismo cliente (ID de la institución)
    if cliente_usuario_a_inactivar.client_uuid != cliente_del_usuario_administrador.client_uuid:
        # Esto es un intento de violación de seguridad (un admin tratando de editar otra escuela)
        raise PermissionError("Acceso denegado: El usuario no pertenece a su institución.")
        
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")
    
    try:
        user.isActive = False
        user.is_disabled_by_client = True
        db.session.commit()
        
        return user
    except Exception as e:
        db.session.rollback()
        raise e
    