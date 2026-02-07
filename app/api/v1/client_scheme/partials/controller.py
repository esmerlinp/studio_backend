from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.partial_list_service import get_partials

@jwt_required()
def get_all():
    """
    Get all partials.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    data = get_partials(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
