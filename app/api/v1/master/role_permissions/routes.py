from flask import Blueprint
from . import controller

role_permissions_bp = Blueprint('role_permissions', __name__, url_prefix='/api/v1/master/role-permissions')

role_permissions_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
role_permissions_bp.add_url_rule('/<int:rp_id>', view_func=controller.get_one, methods=['GET'])
role_permissions_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
role_permissions_bp.add_url_rule('/<int:rp_id>', view_func=controller.update, methods=['PUT'])
role_permissions_bp.add_url_rule('/<int:rp_id>', view_func=controller.delete, methods=['DELETE'])
