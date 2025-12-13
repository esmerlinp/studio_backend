from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app.database import db
from app.services import user_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity



def hashear_password(password):
    return generate_password_hash(password)



@jwt_required()
@track_activity
def me():
    user_id = get_jwt_identity()  # devuelve lo que enviaste como identity
    user = user_service.get_user_by_id(user_id=int(user_id))
    return jsonify({"result": user})


@jwt_required()
@track_activity
def get_users():
    # data = db.fetch_data('SELECT * FROM usuarios')
    users = user_service.get_all_users()
    result = []
    if users:
        result = [user.__dict__ for user in users]
        #return jsonify({"result": result}), 200
    return jsonify({"result": result}), 200



@jwt_required()
@track_activity
def get_user(userId):
    user = user_service.get_user_by_id(user_id=userId)
    if user:
        return jsonify({"result": user}), 200
    
    return jsonify({"result": None}), 200

@jwt_required()
@track_activity
def get_user_by_name(userName):
    user = user_service.get_user_by_user_name(user_name=userName)
    if user:
        return jsonify({"result": user}), 200
    
    return jsonify({"result": None}), 200



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

