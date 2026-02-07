from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.subject_list_service import get_subjects

@jwt_required()
def get_all():
    """
    Get all subjects.
    Supports filtering by subjectAreaId and isActive.
    """
    filters = {}
    
    if request.args.get('subjectAreaId'):
        filters['subjectAreaId'] = request.args.get('subjectAreaId', type=int)

    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'

    data = get_subjects(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
