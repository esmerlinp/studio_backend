from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.screen_functionality_service import (
    get_screen_functionalities, get_screen_functionality_by_id,
    create_screen_functionality, update_screen_functionality, delete_screen_functionality
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([sf.to_dict() for sf in get_screen_functionalities()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(sf_id):
    sf = get_screen_functionality_by_id(sf_id)
    if not sf: return jsonify({"error": "Screen Functionality not found"}), 404
    return jsonify(sf.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="SCREEN_FUNCTIONALITY")
def create():
    try:
        data = request.get_json()
        sf = create_screen_functionality(data)
        return jsonify(sf.to_dict()), 201
    except Exception as e:
        if "Duplicate entry" in str(e) or "UniqueConstraint" in str(e) or "integrity" in str(e).lower():
             return jsonify({"error": "La funcionalidad ya está asignada a esta pantalla."}), 409
        return jsonify({"error": str(e)}), 500

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="SCREEN_FUNCTIONALITY")
def update(sf_id):
    try:
        data = request.get_json()
        sf = update_screen_functionality(sf_id, data)
        if not sf: return jsonify({"error": "Screen Functionality not found"}), 404
        return jsonify(sf.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="SCREEN_FUNCTIONALITY")
def delete(sf_id):
    if delete_screen_functionality(sf_id): return jsonify({"message": "Screen Functionality deleted"}), 200
    return jsonify({"error": "Screen Functionality not found"}), 404
