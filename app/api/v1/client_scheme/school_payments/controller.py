from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.school_payment_service import get_school_payments

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
