from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.phone_type_service import (
    get_phone_types, get_phone_type_by_id,
    create_phone_type, update_phone_type, delete_phone_type
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([pt.to_dict() for pt in get_phone_types()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(pt_id):
    pt = get_phone_type_by_id(pt_id)
    if not pt: return jsonify({"error": "Phone Type not found"}), 404
    return jsonify(pt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="PHONE_TYPE")
def create():
    data = request.get_json()
    pt = create_phone_type(data)
    return jsonify(pt.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="PHONE_TYPE")
def update(pt_id):
    data = request.get_json()
    pt = update_phone_type(pt_id, data)
    if not pt: return jsonify({"error": "Phone Type not found"}), 404
    return jsonify(pt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="PHONE_TYPE")
def delete(pt_id):
    if delete_phone_type(pt_id): return jsonify({"message": "Phone Type deleted"}), 200
    return jsonify({"error": "Phone Type not found"}), 404
