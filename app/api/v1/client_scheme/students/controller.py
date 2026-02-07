from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.student_list_service import get_students
from app.services.client_scheme.student_service import get_full_student_detail

@jwt_required()
def get_all():
    """
    Get all students.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('studentStateId'):
        filters['studentStateId'] = request.args.get('studentStateId', type=int)
        
    data = get_students(filters)
        
    return jsonify([item.to_dict() for item in data]), 200

@jwt_required()
def get_by_id(id):
    """
    Get student by ID with full details.
    """
    data = get_full_student_detail(id)
    if not data:
        return jsonify({'message': 'Estudiante no encontrado'}), 404
        
    return jsonify(data), 200

@jwt_required()
def save(id=None):
    """
    Create or Update student details.
    """
    from app.services.client_scheme.student_service import save_student_detail
    data = request.get_json()
    
    student_id, error_msg = save_student_detail(id, data)
    
    if error_msg:
        return jsonify({'message': error_msg}), 400
        
    return jsonify({'message': 'Estudiante guardado correctamente', 'id': student_id}), 200
