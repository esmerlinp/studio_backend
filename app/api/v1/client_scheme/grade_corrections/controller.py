from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.grade_correction_list_service import get_grade_corrections

@jwt_required()
def get_all():
    """
    Get all grade corrections.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    data = get_grade_corrections(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
