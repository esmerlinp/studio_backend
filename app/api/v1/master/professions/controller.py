from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.profession_service import (
    get_professions, get_profession_by_id,
    create_profession, update_profession, delete_profession
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([p.to_dict() for p in get_professions()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(profession_id):
    profession = get_profession_by_id(profession_id)
    if not profession: return jsonify({"error": "Profession not found"}), 404
    return jsonify(profession.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="PROFESSION")
def create():
    data = request.get_json()
    profession = create_profession(data)
    return jsonify(profession.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="PROFESSION")
def update(profession_id):
    data = request.get_json()
    profession = update_profession(profession_id, data)
    if not profession: return jsonify({"error": "Profession not found"}), 404
    return jsonify(profession.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="PROFESSION")
def delete(profession_id):
    if delete_profession(profession_id): return jsonify({"message": "Profession deleted"}), 200
    return jsonify({"error": "Profession not found"}), 404
