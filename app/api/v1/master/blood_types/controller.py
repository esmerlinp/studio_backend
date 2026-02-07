from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.blood_type_service import (
    get_blood_types, get_blood_type_by_id,
    create_blood_type, update_blood_type, delete_blood_type
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([bt.to_dict() for bt in get_blood_types()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(bt_id):
    bt = get_blood_type_by_id(bt_id)
    if not bt: return jsonify({"error": "Blood Type not found"}), 404
    return jsonify(bt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="BLOOD_TYPE")
def create():
    data = request.get_json()
    bt = create_blood_type(data)
    return jsonify(bt.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="BLOOD_TYPE")
def update(bt_id):
    data = request.get_json()
    bt = update_blood_type(bt_id, data)
    if not bt: return jsonify({"error": "Blood Type not found"}), 404
    return jsonify(bt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="BLOOD_TYPE")
def delete(bt_id):
    if delete_blood_type(bt_id): return jsonify({"message": "Blood Type deleted"}), 200
    return jsonify({"error": "Blood Type not found"}), 404
