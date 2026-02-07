from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.inscription_list_service import get_inscriptions

@jwt_required()
def get_all():
    """
    Get all inscriptions.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    data = get_inscriptions(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
