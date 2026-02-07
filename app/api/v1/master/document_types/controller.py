from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.document_type_service import (
    get_document_types, get_document_type_by_id,
    create_document_type, update_document_type, delete_document_type
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([dt.to_dict() for dt in get_document_types()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(dt_id):
    dt = get_document_type_by_id(dt_id)
    if not dt: return jsonify({"error": "Document Type not found"}), 404
    return jsonify(dt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="DOCUMENT_TYPE")
def create():
    data = request.get_json()
    dt = create_document_type(data)
    return jsonify(dt.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="DOCUMENT_TYPE")
def update(dt_id):
    data = request.get_json()
    dt = update_document_type(dt_id, data)
    if not dt: return jsonify({"error": "Document Type not found"}), 404
    return jsonify(dt.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="DOCUMENT_TYPE")
def delete(dt_id):
    if delete_document_type(dt_id): return jsonify({"message": "Document Type deleted"}), 200
    return jsonify({"error": "Document Type not found"}), 404
