from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor
from app.core import db
from app.models import user_model
from dataclasses import asdict
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middlewares.track_activity import track_activity
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')

def hashear_password(password):
    return generate_password_hash(password)





@usuarios_bp.route('/users', methods=['GET'])
@jwt_required()
@track_activity
def get_users():
    # data = db.fetch_data('SELECT * FROM usuarios')
    users = user_model.get_all_users()
    result = []
    if users:
        result = [user.__dict__ for user in users]
        #return jsonify({"result": result}), 200
    return jsonify({"result": result}), 200



@usuarios_bp.route('/users/<userId>', methods=['GET'])
def get_user_by_id(userId):
    user = user_model.get_user_by_id(user_id=userId)
    if user:
        return jsonify({"result": user}), 200
    
    return jsonify({"result": None}), 200





@usuarios_bp.route('/usuarios', methods=['POST'])
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

