from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.client_scheme.school_payment_service import get_school_payments
from app.services.client_scheme.financial_service import get_pending_charges, get_family_balance, process_payment

@jwt_required()
def get_all():
    """
    Get all school payments.
    """
    filters = {}
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_school_payments(filters)
        
    return jsonify([item.to_dict() for item in data]), 200

@jwt_required()
def get_pending():
    """
    Get pending charges for payment interface.
    """
    filters = {}
    if request.args.get('familyId'):
        filters['familyId'] = request.args.get('familyId', type=int)
        
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_pending_charges(filters)
    return jsonify([item.to_dict() for item in data]), 200

@jwt_required()
def get_balance():
    """
    Get family balance summary.
    """
    family_id = request.args.get('familyId', type=int)
    cycle_id = request.args.get('cycleId', type=int)
    
    if not family_id:
        return jsonify({'message': 'familyId required'}), 400
        
    data = get_family_balance(family_id, cycle_id)
    return jsonify(data), 200

@jwt_required()
def submit_payment():
    """
    Process a new payment.
    """
    user_id = get_jwt_identity()
    data = request.json
    
    try:
        result = process_payment(data, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
