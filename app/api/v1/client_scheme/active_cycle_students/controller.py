from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.active_cycle_student_service import get_active_cycle_students_filtered

@jwt_required()
def get_all():
    """
    Get all active cycle students.
    Supports filtering by studentId, courseId, levelId, and cycleId via query params.
    """
    filters = {}
    
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)
        
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_active_cycle_students_filtered(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
