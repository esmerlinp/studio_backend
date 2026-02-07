from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.concept_list_service import get_concepts

@jwt_required()
def get_all():
    """
    Get all concepts.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    if request.args.get('isFamily') is not None:
        filters['isFamily'] = request.args.get('isFamily').lower() == 'true'
        
    data = get_concepts(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
