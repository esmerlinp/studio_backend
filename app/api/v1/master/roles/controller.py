from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.role_service import (
    get_roles, get_role_by_id, create_role, update_role, delete_role
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([r.to_dict() for r in get_roles()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(role_id):
    role = get_role_by_id(role_id)
    if not role: return jsonify({"error": "Role not found"}), 404
    return jsonify(role.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="ROLE")
def create():
    data = request.get_json()
    role = create_role(data)
    return jsonify(role.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="ROLE")
def update(role_id):
    data = request.get_json()
    role = update_role(role_id, data)
    if not role: return jsonify({"error": "Role not found"}), 404
    return jsonify(role.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="ROLE")
def delete(role_id):
    if delete_role(role_id): return jsonify({"message": "Role deleted"}), 200
    return jsonify({"error": "Role not found"}), 404
