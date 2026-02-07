from flask import request, jsonify
from app import audit_log, require_role
from app.utils.types import ActionType, ResourceTypes
from flask_jwt_extended import jwt_required
from app.services.master_scheme.payment_processor_service import (
    get_payment_processors, get_payment_processor_by_id,
    create_payment_processor, update_payment_processor, delete_payment_processor
)

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_all():
    return jsonify([pp.to_dict() for pp in get_payment_processors()]), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def get_one(pp_id):
    pp = get_payment_processor_by_id(pp_id)
    if not pp: return jsonify({"error": "Payment Processor not found"}), 404
    return jsonify(pp.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.CREATE, resource_type="PAYMENT_PROCESSOR")
def create():
    data = request.get_json()
    pp = create_payment_processor(data)
    return jsonify(pp.to_dict()), 201

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.UPDATE, resource_type="PAYMENT_PROCESSOR")
def update(pp_id):
    data = request.get_json()
    pp = update_payment_processor(pp_id, data)
    if not pp: return jsonify({"error": "Payment Processor not found"}), 404
    return jsonify(pp.to_dict()), 200

@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
@audit_log(action=ActionType.DELETE, resource_type="PAYMENT_PROCESSOR")
def delete(pp_id):
    if delete_payment_processor(pp_id): return jsonify({"message": "Payment Processor deleted"}), 200
    return jsonify({"error": "Payment Processor not found"}), 404
