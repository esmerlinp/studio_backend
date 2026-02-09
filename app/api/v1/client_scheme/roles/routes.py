from flask import Blueprint
from .controller import (
    list_roles, create_role, get_catalog, 
    list_role_permissions, set_role_permissions,
    list_role_users, assign_role_users
)

client_roles_bp = Blueprint('client_roles', __name__)

client_roles_bp.route('/', methods=['GET'])(list_roles)
client_roles_bp.route('/', methods=['POST'])(create_role)
client_roles_bp.route('/catalog', methods=['GET'])(get_catalog)
client_roles_bp.route('/<int:role_id>/permissions', methods=['GET'])(list_role_permissions)
client_roles_bp.route('/<int:role_id>/permissions', methods=['POST'])(set_role_permissions)
client_roles_bp.route('/<int:role_id>/users', methods=['GET'])(list_role_users)
client_roles_bp.route('/<int:role_id>/users', methods=['POST'])(assign_role_users)
