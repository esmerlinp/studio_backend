from flask import Blueprint, request, jsonify
import psycopg2


usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')


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


