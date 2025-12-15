from flask import  request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.database import db   # conexión a BD
from app.services.user_service import get_user_by_user_name_with_passwd, get_user_by_id, close_session
from app.utils.responses import success, error


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

    # TODO: Activar cuando las claves estén encriptadas en la BD
    if not verificar_password(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # TEMPORAL — Contraseñas sin hash
    # if password != user.password:
    #     return error("Invalid password", status_code=401)

    # Crear Access Token con datos NO sensibles
    # identity = {
    #     "userId": user["idusuario"],
    #     "userName": user["susuario"],
    #     "email": user["scorreoelectronico"],
    #     "uuidToken": token_uuid
    # }
    
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
    
    

    db.execute_non_query("""
        INSERT INTO usuariossesiones (idusuario, srefreshtoken, dfechaexpiracion)
        VALUES (%s, %s, NOW() + INTERVAL '%s minutes')
    """, (user.userId, refresh_token, INACTIVITY_MINUTES))
    
    session_id = db.fetch_one("""select idusuariosesion from usuariossesiones 
                                where idusuario=%s and srefreshtoken=%s""",
                                (user.userId, refresh_token))
    
    #TODO: usar este cuando se cree el campo ip en la tabla de sesiones
    # db.execute_non_query("""
    #     INSERT INTO usuariossesiones (idusuario, srefreshtoken, dfechaexpiracion, ssessionip)
    #     VALUES (%s, %s, NOW() + INTERVAL '%s minutes', %s)
    # """, (user.userId, refresh_token, INACTIVITY_MINUTES, request.remote_addr))

    response_data = user.__dict__
    del response_data['password']
    response_data['accessToken'] = access_token
    response_data['refresh_token'] = refresh_token
    response_data['sessionId'] = session_id['idusuariosesion']

    return success(data=response_data, message="Login successful", status_code=200)






def logout(user_id:int, sessionId:int):
    # TODO: gestionar invalidación del token en tabla de sesiones
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
