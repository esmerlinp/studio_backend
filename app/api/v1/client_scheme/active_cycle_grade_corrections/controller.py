from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.active_cycle_grade_correction_service import get_active_cycle_grade_corrections

@jwt_required()
def get_all():
    """
    Get all active cycle grade corrections.
    """
    filters = {}
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('teacherId'):
        filters['teacherId'] = request.args.get('teacherId', type=int)
        
    data = get_active_cycle_grade_corrections(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
