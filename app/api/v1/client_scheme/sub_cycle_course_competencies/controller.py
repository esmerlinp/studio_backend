from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.sub_cycle_course_competency_service import get_sub_cycle_course_competencies

@jwt_required()
def get_all():
    """
    Get all sub cycle course competencies.
    """
    filters = {}
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('subCycleId'):
        filters['subCycleId'] = request.args.get('subCycleId', type=int)
        
    if request.args.get('subjectId'):
        filters['subjectId'] = request.args.get('subjectId', type=int)
        
    data = get_sub_cycle_course_competencies(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
