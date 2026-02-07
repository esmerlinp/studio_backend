from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.role_permission_service import (
    get_role_permissions, get_role_permission_by_id,
    create_role_permission, update_role_permission, delete_role_permission
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([rp.to_dict() for rp in get_role_permissions()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(rp_id):
    rp = get_role_permission_by_id(rp_id)
    if not rp: return jsonify({"error": "Role Permission not found"}), 404
    return jsonify(rp.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="ROLE_PERMISSION")
def create():
    data = request.get_json()
    rp = create_role_permission(data)
    return jsonify(rp.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="ROLE_PERMISSION")
def update(rp_id):
    data = request.get_json()
    rp = update_role_permission(rp_id, data)
    if not rp: return jsonify({"error": "Role Permission not found"}), 404
    return jsonify(rp.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="ROLE_PERMISSION")
def delete(rp_id):
    if delete_role_permission(rp_id): return jsonify({"message": "Role Permission deleted"}), 200
    return jsonify({"error": "Role Permission not found"}), 404
