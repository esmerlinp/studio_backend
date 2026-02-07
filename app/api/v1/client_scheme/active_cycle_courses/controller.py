from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.active_cycle_course_service import get_active_cycle_courses, get_active_cycle_courses_filtered

@jwt_required()
def get_all():
    """
    Get all active cycle courses.
    Supports filtering by cycle_id and course_id via query params.
    """
    cycle_id = request.args.get('cycleId', type=int)
    course_id = request.args.get('courseId', type=int)
    
    if cycle_id or course_id:
        data = get_active_cycle_courses_filtered(cycle_id, course_id)
    else:
        data = get_active_cycle_courses()
        
    return jsonify([item.to_dict() for item in data]), 200
