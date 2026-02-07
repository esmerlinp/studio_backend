from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.child_discount_service import get_child_discounts

@jwt_required()
def get_all():
    """
    Get all child discounts.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_child_discounts(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
