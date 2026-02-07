from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.tax_list_service import get_taxes

@jwt_required()
def get_all():
    """
    Get all taxes.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    data = get_taxes(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
