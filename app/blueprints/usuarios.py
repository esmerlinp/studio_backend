from flask import Blueprint, request

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')

@usuarios_bp.route('/perfil', methods=['GET'])
def perfil():
    return 'Perfil de usuarios'


@usuarios_bp.route('/perfil')
def buscar():
    query = request.args.get('q')
    return f'Buscando: {query or "nada"}'