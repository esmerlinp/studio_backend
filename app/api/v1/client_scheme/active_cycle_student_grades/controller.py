from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.active_cycle_student_grade_service import get_active_cycle_student_grades

@jwt_required()
def get_all():
    """
    Get all active cycle student grades.
    """
    filters = {}
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('subjectId'):
        filters['subjectId'] = request.args.get('subjectId', type=int)
        
    data = get_active_cycle_student_grades(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
