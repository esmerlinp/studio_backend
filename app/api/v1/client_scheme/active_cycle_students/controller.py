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
        
    if request.args.get('search'):
        filters['search'] = request.args.get('search')
        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = get_active_cycle_students_filtered(filters)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    items = []
    for row in pagination.items:
        # row is a tuple containing the columns added in the service via .add_columns()
        items.append({
            "studentCycleClassroomId": row[0],
            "studentCode": row[1],
            "studentName": row[2],
            "courseName": row[3],
            "classroomName": row[4],
            "studentStatus": row[5],
            "responsibleName": row[6],
            "responsiblePhone": row[7],
            "id": row[8]
        })
        
    return jsonify({
        "items": items,
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page
    }), 200
