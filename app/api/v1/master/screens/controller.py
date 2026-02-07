from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.screen_service import (
    get_screens, get_screen_by_id, create_screen, update_screen, delete_screen
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([s.to_dict() for s in get_screens()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(screen_id):
    screen = get_screen_by_id(screen_id)
    if not screen: return jsonify({"error": "Screen not found"}), 404
    return jsonify(screen.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="SCREEN")
def create():
    data = request.get_json()
    screen = create_screen(data)
    return jsonify(screen.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="SCREEN")
def update(screen_id):
    data = request.get_json()
    screen = update_screen(screen_id, data)
    if not screen: return jsonify({"error": "Screen not found"}), 404
    return jsonify(screen.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="SCREEN")
def delete(screen_id):
    if delete_screen(screen_id): return jsonify({"message": "Screen deleted"}), 200
    return jsonify({"error": "Screen not found"}), 404
