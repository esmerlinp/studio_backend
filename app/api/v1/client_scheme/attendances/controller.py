from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.attendance_list_service import get_attendances, get_attendance_checklist, save_bulk_attendance

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

@jwt_required()
def get_checklist():
    """
    Get student checklist for attendance for a specific class and date.
    Query params: date (YYYY-MM-DD), levelId, courseId, classroomId.
    """
    filters = {
        'date': request.args.get('date'),
        'levelId': request.args.get('levelId', type=int),
        'courseId': request.args.get('courseId', type=int),
        'classroomId': request.args.get('classroomId', type=int)
    }
    
    if not filters['date']:
        return jsonify({"msg": "Missing date parameter"}), 400
        
    data = get_attendance_checklist(filters)
    return jsonify(data), 200

@jwt_required()
def bulk_save():
    """
    Save or update multiple attendance records.
    Expects a JSON body: { "data": [{studentCycleClassroomId, date, attendanceTypeId, comment}, ...] }
    """
    payload = request.get_json()
    if not payload or 'data' not in payload:
        return jsonify({"msg": "Missing data"}), 400
        
    results = save_bulk_attendance(payload['data'])
    return jsonify({"msg": "Success", "count": len(results)}), 200
