from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor
from app.core import db

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')

def hashear_password(password):
    return generate_password_hash(password)

def verificar_password(hash_stored, password):
    return check_password_hash(hash_stored, password)



@usuarios_bp.route('/usuarios', methods=['GET'])
def get_users():
    data = db.fetch_data('SELECT * FROM usuarios')
    return data
    #return jsonify(usuarios)



@usuarios_bp.route('/usuarios/<id>', methods=['GET'])
def get_user_by_id(id):
    data = db.fetch_one("select * from usuarios where idusuario =%s", params=(id,))
    return data




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

