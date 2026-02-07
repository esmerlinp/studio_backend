from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.gender_service import (
    get_genders, get_gender_by_id, create_gender, update_gender, delete_gender
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([g.to_dict() for g in get_genders()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(gender_id):
    gender = get_gender_by_id(gender_id)
    if not gender: return jsonify({"error": "Gender not found"}), 404
    return jsonify(gender.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="GENDER")
def create():
    data = request.get_json()
    gender = create_gender(data)
    return jsonify(gender.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="GENDER")
def update(gender_id):
    data = request.get_json()
    gender = update_gender(gender_id, data)
    if not gender: return jsonify({"error": "Gender not found"}), 404
    return jsonify(gender.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="GENDER")
def delete(gender_id):
    if delete_gender(gender_id): return jsonify({"message": "Gender deleted"}), 200
    return jsonify({"error": "Gender not found"}), 404
