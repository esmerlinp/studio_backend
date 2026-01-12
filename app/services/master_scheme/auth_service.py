from flask import  request, jsonify, g
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta, datetime
from app.services.master_scheme.user_service import get_user_by_user_name_with_passwd, get_user_by_id, get_user_preferences, add_default_user_preferences
from app.services.master_scheme.session_service import close_session, create_session, get_session_active_by_refresh_token
from app.utils.responses import success, error
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.exceptions import AuditedError
from app import log_action, INACTIVITY_MINUTES
from app.utils.types import ResourceTypes, ActionType, Roles as r, states
from app.utils.helpers import send_email_template
from app.utils import i18n
from dotenv import load_dotenv
import os

JWT_ACCESS_TOKEN_EXPIRES = 24   # horas


# -----------------------------
# Helpers
# -----------------------------

def validar_login_payload(data):
    """Valida que el payload contenga los campos requeridos."""
    if not data:
        return i18n._("error.auth.empty_payload")

    if not data.get("username"):
        return i18n._("error.auth.empty_username")

    if not data.get("password"):
        return i18n._("error.auth.empty_password")

    return None



# -----------------------------
# Rutas
# -----------------------------

def login():
    load_dotenv()
    app_name = os.getenv("APP_NAME")
    data = request.json
    error_data = validar_login_payload(data)
    

    if error_data:
        return jsonify({"error": error_data}), 400

    username = data["username"]
    password = data["password"]


    user = get_user_by_user_name_with_passwd(user_name=username)


    if not user:
        return error(i18n._("error.auth.invalid_credentials"), status_code=401)

    g.user_id = user.userId
    relacion = UsuarioCliente.query.filter_by(user_id=user.userId).first()
    client = Client.query.filter_by(uuid=relacion.client_uuid).first()
    if client:
        g.scheme = client.schemaName

    if not check_password_hash(user.password, password):
        raise AuditedError(i18n._("error.auth.invalid_credentials"),
                            resource_type=ResourceTypes.USER_SESSION,
                            action_type=ActionType.LOGIN, user_id=user.userId, status_code=401)

    
    is_restore = False

    if not user.isActive:
        if user.rol in (r.OWNER, r.ADMIN):
            if not client.isActive:
                trans = PaymentTransaction.query.filter_by(clientId=client.clientId, status=states.APPROVED).all()
                if trans:
                    is_restore = True
                    clientId = client.clientId

        else:            
            # Personalizamos el mensaje según el contexto (si tienes el campo de motivo)
            mensaje_error = i18n._("error.auth.account_inactive_detail")
            return error(message=mensaje_error, status_code=401) # 403 Forbidden es más preciso que 400


    identity = str(user.userId)   # identity debe ser string


    
    refresh_token = create_refresh_token(identity=identity)
    
    
    session = create_session(userId=user.userId, refreshToken=refresh_token, inactivity_minutes=INACTIVITY_MINUTES, ipAddress=request.remote_addr, userAgent=request.user_agent.string)
    if session is None:
        return error(i18n._("error.auth.session_creation_failed"), status_code=500)
    
    session_create = get_session_active_by_refresh_token(refreshToken=refresh_token)
    preferences = get_user_preferences(user_id=user.userId)
    if not preferences:
        new_pref = add_default_user_preferences(user_id=user.userId)
        if not new_pref:
            return error(i18n._("error.auth.preferences_error"), status_code=500)
        preferences = new_pref
            
    
    # ACCESS TOKEN con claims adicionales
    lang = preferences.preferences.get("language", "es")
    access_token = create_access_token(
        identity=identity,
        expires_delta=timedelta(hours=24),
        additional_claims={
            "username": user.username,
            "email": user.email,
            "language": lang,
            "hourFormat": preferences.preferences.get("hourFormat", 24),
            "timezone": preferences.preferences.get("timezone", "UTC"),
            "dateFormat": preferences.preferences.get("dateFormat", "DD-MM-YYYY"),
        }
    )

    response_data = user.to_dict()
    response_data['accessToken'] = access_token
    response_data['refresh_token'] = refresh_token
    response_data['sessionId'] = session_create.sessionId
    response_data['preferences'] = preferences.preferences
    
    if is_restore:  
        return error(message=i18n._("error.auth.subscription_expired"),
                data={"access_token":access_token},
                redirect_url=f"/billing/restore?clientId={clientId}&token={access_token}", 
                status_code=403)               

    
    send_email_template(subject=i18n._("email.subject.login_notification"), 
                        to=[user.email], 
                        path_template=f"emails/{lang}/notification_login.html",
                        app_name=app_name,
                        nombre_usuario=user.firstName,
                        ip_address=session_create.ipAddress,
                        dispositivo=session_create.userAgent,
                        fecha_hora=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        email_usuario=user.email
                        )
    
    log_action(action=ActionType.LOGIN, resource_type=ResourceTypes.USER_SESSION,
                resource_id=user.userId, description="Login successful", user_id=user.userId)
    
    return success(data=response_data, message=i18n._("success.auth.login"), status_code=200)






def logout(user_id:int, sessionId:int):

    result = close_session(sessionId=sessionId, user_id=user_id)
    if sessionId != result.get("sessionId", 0):
        return error(i18n._("error.auth.session_not_found"), status_code=404)
        
    return success(data={"sessionId": sessionId}, message="Logout successful", status_code=200) 






def refresh_token(user_id: int):
    user = get_user_by_id(user_id=int(user_id))
    if not user:
        return error(i18n._("error.auth.user_not_found"), status_code=404)
    
    additional_claims={
        "username": user.username,
        "email": user.email,
    }
    
    new_access_token = create_access_token(identity=user_id,  
                                           expires_delta=timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES), 
                                           additional_claims=additional_claims
                                        )
    if not new_access_token:
        return error(i18n._("error.auth.token_generation_failed"), status_code=500)
    
    result = {
        "accessToken": new_access_token
    }
    return result
