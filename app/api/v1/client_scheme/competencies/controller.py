from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.competency_list_service import get_competencies

@jwt_required()
def get_all():
    """
    Get all competencies.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    data = get_competencies(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
