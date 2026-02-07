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

@jwt_required()
def get_checklist():
    """
    Get students and their grades for a specific subject/partial/course.
    """
    filters = {
        'cycleId': request.args.get('cycleId', type=int),
        'courseId': request.args.get('courseId', type=int),
        'subjectId': request.args.get('subjectId', type=int),
        'partialId': request.args.get('partialId', type=int),
        'classroomId': request.args.get('classroomId', type=int)
    }
    
    if not all([filters['cycleId'], filters['courseId'], filters['subjectId'], filters['partialId']]):
        return jsonify({"error": "Missing required filters"}), 400
        
    from app.services.client_scheme.active_cycle_student_grade_service import get_grades_checklist
    data = get_grades_checklist(filters)
    return jsonify(data), 200

@jwt_required()
def save_bulk():
    """
    Bulk save grades.
    """
    data = request.get_json()
    if not data or 'data' not in data:
        return jsonify({"error": "Invalid payload"}), 400
        
    from app.services.client_scheme.active_cycle_student_grade_service import save_grades
    results = save_grades(data['data'])
    return jsonify({"message": "Grades saved", "count": len(results)}), 200
