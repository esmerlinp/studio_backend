from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.attendance_list_service import get_attendances

@jwt_required()
def get_all():
    """
    Get all attendances.
    Supports filtering by studentId, courseId, and date.
    """
    filters = {}
    
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('date'):
        filters['date'] = request.args.get('date')
        
    data = get_attendances(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
