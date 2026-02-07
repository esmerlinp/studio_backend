from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.payment_calendar_list_service import get_payment_calendar

@jwt_required()
def get_all():
    """
    Get all payment calendar entries.
    Supports filtering by cycleId.
    """
    filters = {}
    
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_payment_calendar(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
