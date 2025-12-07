from flask import Blueprint, request, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor




usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')


def hashear_password(password):
    return generate_password_hash(password)

def verificar_password(hash_stored, password):
    return check_password_hash(hash_stored, password)



def get_db_connection():
    return psycopg2.connect(
        host='ep-morning-wildflower-addmvwux.c-2.us-east-1.aws.neon.tech',
        database='AKDMIA_CLIENTE',
        user='neondb_owner',
        password='npg_fFT1cLH8gjuy'
    )




@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tblcomun')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(usuarios)


@usuarios_bp.route('/perfil', methods=['GET'])
def perfil():
    return 'Perfil de usuarios'





@usuarios_bp.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    password_encriptada = hashear_password(data['password'])
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s) RETURNING id",
        (data['nombre'], data['email'], password_encriptada)
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'mensaje': 'Usuario creado', 'id': nuevo_id}), 201




@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT password FROM usuarios WHERE email = %s", (data['email'],))
    usuario = cur.fetchone()
    
    if usuario and verificar_password(usuario['password'], data['password']):
        return jsonify({'mensaje': 'Login exitoso'})
    return jsonify({'error': 'Credenciales inválidas'}), 401

