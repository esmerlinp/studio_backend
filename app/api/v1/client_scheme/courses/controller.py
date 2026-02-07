from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.course_list_service import get_courses

@jwt_required()
def get_all():
    """
    Get all courses.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    if request.args.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)
        
    data = get_courses(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
