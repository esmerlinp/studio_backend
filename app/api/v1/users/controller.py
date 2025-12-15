from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.database import db
from app.services import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity
from app.utils.responses import success, error
from app.utils.helpers import generate_reset_token, send_reset_email
from flask import current_app

def hashear_password(password):
    return generate_password_hash(password)



@jwt_required()
@track_activity
def me():
    user_id = get_jwt_identity()  # devuelve lo que enviaste como identity
    user = user_service.get_user_by_id(user_id=int(user_id))
    if not user:
        return error("User not found", status_code=404)
    
    return success(data=user, message="User retrieved successfully", status_code=200)



@jwt_required()
@track_activity
def get_users():
    # data = db.fetch_data('SELECT * FROM usuarios')
    users = user_service.get_all_users()
    result = []
    if users:
        result = [user.__dict__ for user in users]
        #return jsonify({"result": result}), 200
    return success(data=result, message="Users retrieved successfully", status_code=200)



@jwt_required()
@track_activity
def get_user(userId):
    user = user_service.get_user_by_id(user_id=userId)
    return success(data=user, message="User retrieved successfully", status_code=200)

@jwt_required()
@track_activity
def get_user_by_name(userName):
    user = user_service.get_user_by_user_name(user_name=userName)
    return success(data=user, message="User retrieved successfully", status_code=200)


@jwt_required()
@track_activity
def change_password():
    try:
        new_password = request.json.get('new_password')
        sessionId = request.json.get('sessionId')
        
        identity = get_jwt_identity()     # recupera el mismo identity guardado en el refresh token
        result = user_service.change_user_password(user_id=int(identity), new_password=new_password, sessionId=sessionId)
        if not result:
            return error(message="User not found or password not changed", status_code=404)
        
        return success(data=result, message="Password changed successfully", status_code=200)
    
       
        
        
    except Exception as e:
        return error(message=str(e), status_code=500)






def forgot_password():
    email = request.json.get("email")

    user = user_service.get_user_by_email(email=email)
    if not user:
        # No reveles si el usuario existe
        return {"message": "Si el correo existe, se enviará un enlace"}, 200

    token = generate_reset_token(user.userId)
    print(f"Generated token: {token}")
    #reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
    
    send_reset_email(email="epaniagua@camsoft.com.do", token=token, userName=user.firstName)

    return {"message": "Si el correo existe, se enviará un enlace"}, 200


@jwt_required()
@track_activity
def create_user():
    data = request.json
    password_encriptada = hashear_password(data['password'])
    
    filas = db.execute_non_query(
        """
        INSERT INTO usuarios (
            bactivo,
            bbloqueado,
            bcambiarcontrasena,
            busuarioconfirmado,
            dexpiraciontoken,
            dfechabloqueo,
            dfechaultcambiocont,
            dultimologin,
            iintentoslogin,
            sapellidos,
            scontrasena,
            scorreoelectronico,
            sfoto,
            snombres,
            stokenrecuperacion,
            susuario
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING idusuario
        """,
        (
            data["activo"],
            data["bloqueado"],
            data["cambiarcontrasena"],
            data["usuarioconfirmado"],
            data["expiraciontoken"],     # null → None
            data["fechabloqueo"],        # null → None
            data["fechaultcambiocont"],
            data["ultimologin"],         # null → None
            data["intentoslogin"],
            data["apellidos"],
            password_encriptada,
            data["correoelectronico"],
            data["foto"],                # null → None
            data["nombres"],
            data["tokenrecuperacion"],   # null → None
            data["usuario"]
        )
    )
    return filas













# @usuarios_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     conn = get_db_connection()
#     cur = conn.cursor(cursor_factory=RealDictCursor)
#     cur.execute("SELECT password FROM usuarios WHERE email = %s", (data['email'],))
#     usuario = cur.fetchone()
    
#     if usuario and verificar_password(usuario['password'], data['password']):
#         return jsonify({'mensaje': 'Login exitoso'})
#     return jsonify({'error': 'Credenciales inválidas'}), 401

