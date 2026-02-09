from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import require_permission, audit_log
from app.utils.types import ActionType
from app.services.client_scheme.role_service import (
    get_roles_by_client, create_role_for_client, 
    update_role_permissions, get_role_permissions,
    get_permission_catalog, get_role_users, assign_users_to_role
)
from app.services.master_scheme.user_client_service import get_client_by_user

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "CONSULTAR")
def list_roles():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id)
    if not client:
        return jsonify({"error": "No client context found"}), 400
    
    roles = get_roles_by_client(str(client.uuid))
    return jsonify([r.to_dict() for r in roles]), 200

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "CONSULTAR")
def get_catalog():
    """
    Exposes the system-wide catalog of screens and functionalities.
    """
    catalog = get_permission_catalog()
    return jsonify(catalog), 200

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "CREAR")
@audit_log(action=ActionType.CREATE, resource_type="CLIENT_ROLE")
def create_role():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id)
    if not client:
        return jsonify({"error": "No client context found"}), 400
    
    data = request.get_json()
    role = create_role_for_client(str(client.uuid), data)
    return jsonify(role.to_dict()), 201

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "CONSULTAR")
def list_role_permissions(role_id):
    perms = get_role_permissions(role_id)
    return jsonify([p.to_dict() for p in perms]), 200

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "EDITAR")
@audit_log(action=ActionType.UPDATE, resource_type="CLIENT_ROLE_PERMISSIONS")
def set_role_permissions(role_id):
    data = request.get_json() # Expected list of permissions
    permissions = data.get('permissions', [])
    update_role_permissions(role_id, permissions)
    return jsonify({"message": "Permissions updated successfully"}), 200

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "CONSULTAR")
def list_role_users(role_id):
    """
    Lista los usuarios asignados a un rol.
    """
    users = get_role_users(role_id)
    return jsonify(users), 200

@jwt_required()
@require_permission("SC_ROLES_CLIENTE", "EDITAR")
@audit_log(action=ActionType.UPDATE, resource_type="CLIENT_ROLE_USERS")
def assign_role_users(role_id):
    """
    Asigna usuarios a un rol.
    """
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    assign_users_to_role(role_id, user_ids)
    return jsonify({"message": "Users assigned successfully"}), 200
