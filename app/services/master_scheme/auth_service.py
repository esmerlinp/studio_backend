from flask import  request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.services.master_scheme.user_service import get_user_by_user_name_with_passwd, get_user_by_id, get_user_preferences, add_default_user_preferences
from app.services.master_scheme.session_service import close_session, create_session, get_session_active_by_refresh_token
from app.utils.responses import success, error
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction

from app.utils.helpers import send_email_template
from dotenv import load_dotenv
import os

INACTIVITY_MINUTES = 10  # tiempo de inactividad permitido
JWT_ACCESS_TOKEN_EXPIRES = 24   # horas


# -----------------------------
# Helpers
# -----------------------------
def verificar_password(hash_stored: str, password: str) -> bool:
    """Verifica la contraseña comparando con el hash almacenado."""
    return check_password_hash(hash_stored, password)


def validar_login_payload(data):
    """Valida que el payload contenga los campos requeridos."""
    if not data:
        return "Empty request payload"

    if not data.get("username"):
        return "Empty username"

    if not data.get("password"):
        return "Empty password"

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

    # Consulta del usuario
    # user = db.fetch_one(
    #     "SELECT * FROM usuarios WHERE susuario = %s",
    #     (username,)
    # )
    user = get_user_by_user_name_with_passwd(user_name=username)


    if not user:
        return error("Invalid username or password", status_code=401)

    if not verificar_password(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    is_restore = False
    clientId=0
    if not user.isActive:
        if user.rol in ("OWNER", "ADMIN"):
            relacion = UsuarioCliente.query.filter_by(user_id=user.userId).first()
            client = Client.query.filter_by(uuid=relacion.client_uuid).first()
            if not client.isActive:
                trans = PaymentTransaction.query.filter_by(clientId=client.clientId, status="APPROVED").all()
                if trans:
                    is_restore = True
                    clientId = client.clientId

        else:            
            # Personalizamos el mensaje según el contexto (si tienes el campo de motivo)
            mensaje_error = (
                "Tu cuenta se encuentra inactiva. "
                "Esto puede deberse a un pago pendiente o a una revisión administrativa. "
                "Por favor, contacta al administrador de tu institución o a nuestro equipo de soporte."
            )
            return error(message=mensaje_error, status_code=401) # 403 Forbidden es más preciso que 400


    identity = str(user.userId)   # identity debe ser string

    # ACCESS TOKEN con claims adicionales
    access_token = create_access_token(
        identity=identity,
        expires_delta=timedelta(hours=24),
        additional_claims={
            "username": user.username,
            "email": user.email,
        }
    )
    
    refresh_token = create_refresh_token(identity=identity)
    
    
    session = create_session(userId=user.userId, refreshToken=refresh_token, inactivity_minutes=INACTIVITY_MINUTES, ipAddress=request.remote_addr, userAgent=request.user_agent.string)
    if session is None:
        return error("Error creating user session", status_code=500)
    
    session_create = get_session_active_by_refresh_token(refreshToken=refresh_token)
    preferences = get_user_preferences(user_id=user.userId)
    if not preferences:
        new_pref = add_default_user_preferences(user_id=user.userId)
        if not new_pref:
             return error("Error creating user preferences", status_code=500)
        preferences = new_pref
            
    
    

    response_data = user.to_dict()
    response_data['accessToken'] = access_token
    response_data['refresh_token'] = refresh_token
    response_data['sessionId'] = session_create.sessionId
    response_data['preferences'] = preferences.preferences
    
    if is_restore:                 
        # return error(message="Tu suscripción ha expirado. Por favor, reanúdala para continuar.", 
        #             access_token=access_token, 
        #             status_code=403, redirect_url="/billing/restore") # 403 Forbidden es más preciso que 400
        return jsonify({
            "success": False,
            "msg": "Tu suscripción ha expirado. Por favor, reanúdala para continuar.",
            "access_token":access_token,
            "clientId":clientId,
            "redirect_url":f"/billing/restore?clientId={clientId}&token={access_token}"
            
        }), 403
    from datetime import datetime
    send_email_template(subject="Notificación de Inicio de Sesión", 
                        to=[user.email], 
                        path_template="emails/es/notification_login.html",
                        app_name=app_name,
                        nombre_usuario=user.firstName,
                        ip_address=session_create.ipAddress,
                        dispositivo=session_create.userAgent,
                        fecha_hora=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        email_usuario=user.email
                        )
    return success(data=response_data, message="Login successful", status_code=200)






def logout(user_id:int, sessionId:int):

    result = close_session(sessionId=sessionId, user_id=user_id)
    if sessionId != result.get("sessionId", 0):
        return error("Session not found or already closed", status_code=404)
        
    return success(data={"sessionId": sessionId}, message="Logout successful", status_code=200) 






def refresh_token(user_id: int):
    user = get_user_by_id(user_id=int(user_id))
    if not user:
        return error("User not found", status_code=404)
    
    additional_claims={
        "username": user.username,
        "email": user.email,
    }
    
    new_access_token = create_access_token(identity=user_id,  
                                           expires_delta=timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES), 
                                           additional_claims=additional_claims
                                        )
    if not new_access_token:
        return error("Error generating new token", status_code=500)
    
    result = {
        "accessToken": new_access_token
    }
    return result
