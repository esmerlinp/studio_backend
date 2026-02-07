from flask import Blueprint
from . import controller

roles_bp = Blueprint('master_roles', __name__, url_prefix='/api/v1/master/roles')

roles_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
roles_bp.add_url_rule('/<int:role_id>', view_func=controller.get_one, methods=['GET'])
roles_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
roles_bp.add_url_rule('/<int:role_id>', view_func=controller.update, methods=['PUT'])
roles_bp.add_url_rule('/<int:role_id>', view_func=controller.delete, methods=['DELETE'])
