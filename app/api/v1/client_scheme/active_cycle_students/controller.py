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

@jwt_required()
def get_assignment_board():
    """
    Get students grouped by classroom for assignment board.
    """
    course_id = request.args.get('courseId', type=int)
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400
        
    from app.services.client_scheme.active_cycle_student_service import get_students_by_course_grouped
    data = get_students_by_course_grouped(course_id)
    return jsonify(data), 200

@jwt_required()
def assign_classroom():
    """
    Assign a student to a classroom.
    Payload: { studentCycleClassroomId, classroomId }
    """
    data = request.get_json()
    student_cycle_classroom_id = data.get('studentCycleClassroomId')
    classroom_id = data.get('classroomId')
    
    if not student_cycle_classroom_id:
        return jsonify({"error": "Student ID is required"}), 400
        
    # classroom_id can be null if moving to unassigned
    
    from app.services.client_scheme.active_cycle_student_service import update_student_classroom
    try:
        update_student_classroom(student_cycle_classroom_id, classroom_id)
        return jsonify({"message": "Assigned successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
def bulk_assign_classrooms():
    """
    Bulk assign students to classrooms.
    Payload: { assignments: [ { studentCycleClassroomId, classroomId } ] }
    """
    data = request.get_json()
    assignments = data.get('assignments', [])
    
    if not assignments:
        return jsonify({"error": "No assignments provided"}), 400
        
    from app.services.client_scheme.active_cycle_student_service import update_student_classrooms_bulk
    try:
        update_student_classrooms_bulk(assignments)
        return jsonify({"message": "Bulk assignment completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
def auto_assign():
    """
    Trigger automatic classroom assignment SP.
    Payload: { courseId }
    """
    data = request.get_json()
    course_id = data.get('courseId')
    
    if not course_id:
        return jsonify({"error": "Course ID is required"}), 400
        
    from app.services.client_scheme.active_cycle_student_service import assign_classrooms_automatically
    try:
        assign_classrooms_automatically(course_id)
        return jsonify({"message": "Automatic assignment completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
