from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.core import db   # conexión a BD
from app.models import user_model
from uuid import uuid4

auth_bp = Blueprint('auth', __name__)


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
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    error = validar_login_payload(data)

    if error:
        return jsonify({"error": error}), 400

    username = data["username"]
    password = data["password"]

    # Consulta del usuario
    # user = db.fetch_one(
    #     "SELECT * FROM usuarios WHERE susuario = %s",
    #     (username,)
    # )
    user = user_model.get_user_by_user_name_with_passwd(user_name=username)


    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # TODO: Activar cuando las claves estén encriptadas en la BD
    # if not verificar_password(user['scontrasena'], password):
    #     return jsonify({"error": "Credenciales inválidas"}), 401

    # TEMPORAL — Contraseñas sin hash
    if password != user.password:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Crear Access Token con datos NO sensibles
    # identity = {
    #     "userId": user["idusuario"],
    #     "userName": user["susuario"],
    #     "email": user["scorreoelectronico"],
    #     "uuidToken": token_uuid
    # }
    
    identity = str(user.userId)   # identity debe ser string

    # ACCESS TOKEN con claims adicionales
    token_uuid = str(uuid4())
    access_token = create_access_token(
        identity=identity,
        additional_claims={
            "username": user.username,
            "email": user.email,
            "uuidToken": token_uuid
        }
    )
    
    refresh_token = create_refresh_token(identity=identity)
    
    

    db.execute_non_query("""
        INSERT INTO usuariossesiones (idusuario, srefreshtoken, dfechaexpiracion)
        VALUES (%s, %s, NOW() + INTERVAL '3 minutes')
    """, (user.userId, refresh_token))

    response_data = user.__dict__
    del response_data['password']
    response_data['accessToken'] = access_token
    response_data['refresh_token'] = refresh_token

    # response_data = {
    #     "accessToken": access_token,
    #     "refreshToken": refresh_token,
    #     "userId": user['idusuario'],
    #     "firstName": user['snombres'],
    #     "lastName": user['sapellidos'],
    #     "email": user['scorreoelectronico'],
    #     "username": user['susuario'],

    #     "isActive": user['bactivo'],
    #     "isBlocked": user['bbloqueado'],
    #     "mustChangePassword": user['bcambiarcontrasena'],
    #     "isConfirmed": user['busuarioconfirmado'],

    #     "loginAttempts": user['iintentoslogin'],

    #     "lastPasswordChangeDate": user['dfechaultcambiocont'],
    #     "tokenExpirationDate": user['dexpiraciontoken'],
    #     "blockedDate": user['dfechabloqueo'],
    #     "lastLoginDate": user['dultimologin']
    # }

    return jsonify({"result": response_data}), 200




@auth_bp.route('/logout', methods=['POST'])
def logout():
    # TODO: gestionar invalidación del token en tabla de sesiones
    return jsonify({"result": "ok"}), 200






@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
    new_access_token = create_access_token(identity=identity)
    result = {
        "accessToken": new_access_token
    }
    return jsonify({'result': result}), 200
