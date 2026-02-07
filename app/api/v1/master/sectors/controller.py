from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.sector_service import (
    get_sectors, get_sector_by_id, create_sector, update_sector, delete_sector
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([s.to_dict() for s in get_sectors()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(sector_id):
    sector = get_sector_by_id(sector_id)
    if not sector: return jsonify({"error": "Sector not found"}), 404
    return jsonify(sector.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="SECTOR")
def create():
    data = request.get_json()
    sector = create_sector(data)
    return jsonify(sector.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="SECTOR")
def update(sector_id):
    data = request.get_json()
    sector = update_sector(sector_id, data)
    if not sector: return jsonify({"error": "Sector not found"}), 404
    return jsonify(sector.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="SECTOR")
def delete(sector_id):
    if delete_sector(sector_id): return jsonify({"message": "Sector deleted"}), 200
    return jsonify({"error": "Sector not found"}), 404
