from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.attendance_type_service import (
    get_attendance_types, get_attendance_type_by_id,
    create_attendance_type, update_attendance_type, delete_attendance_type
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([at.to_dict() for at in get_attendance_types()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(at_id):
    at = get_attendance_type_by_id(at_id)
    if not at: return jsonify({"error": "Attendance Type not found"}), 404
    return jsonify(at.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="ATTENDANCE_TYPE")
def create():
    data = request.get_json()
    at = create_attendance_type(data)
    return jsonify(at.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="ATTENDANCE_TYPE")
def update(at_id):
    data = request.get_json()
    at = update_attendance_type(at_id, data)
    if not at: return jsonify({"error": "Attendance Type not found"}), 404
    return jsonify(at.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="ATTENDANCE_TYPE")
def delete(at_id):
    if delete_attendance_type(at_id): return jsonify({"message": "Attendance Type deleted"}), 200
    return jsonify({"error": "Attendance Type not found"}), 404
