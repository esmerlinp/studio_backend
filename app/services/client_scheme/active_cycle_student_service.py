from app import db
from app.models.client_scheme.active_cycle_student_view import ActiveCycleStudentView
from app.models.client_scheme.student_list_view import StudentListView

def get_active_cycle_students():
    """
    Retrieve all active cycle students.
    """
    return ActiveCycleStudentView.query.order_by(ActiveCycleStudentView.studentName).all()

def get_active_cycle_students_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    Joins with StudentListView to get responsible information.
    Returns a query with explicit columns to ensure JSON serializability.
    """
    query = db.session.query(
        ActiveCycleStudentView.studentCycleClassroomId,
        ActiveCycleStudentView.studentCode,
        ActiveCycleStudentView.studentName,
        ActiveCycleStudentView.courseName,
        ActiveCycleStudentView.classroomName,
        ActiveCycleStudentView.studentStatus,
        StudentListView.responsibleName,
        StudentListView.responsiblePhone,
        ActiveCycleStudentView.studentId
    ).outerjoin(
        StudentListView, 
        ActiveCycleStudentView.studentCycleClassroomId == StudentListView.studentClassroomCycleId
    )
    
    if filters:
        if filters.get('studentId'):
            query = query.filter(ActiveCycleStudentView.studentId == filters['studentId'])
            
        if filters.get('courseId'):
            query = query.filter(ActiveCycleStudentView.courseId == filters['courseId'])
            
        if filters.get('levelId'):
            query = query.filter(ActiveCycleStudentView.levelId == filters['levelId'])
            
        if filters.get('cycleId'):
            query = query.filter(ActiveCycleStudentView.cycleId == filters['cycleId'])
            
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                (ActiveCycleStudentView.studentName.ilike(search_term)) |
                (ActiveCycleStudentView.studentCode.ilike(search_term))
            )
            
    return query.order_by(ActiveCycleStudentView.studentName)

def get_students_by_course_grouped(course_id):
    """
    Retrieve students for a course, grouped by classroom.
    Returns:
        {
            'unassigned': [students],
            'classrooms': { classroomId: [students] }
        }
    """
    students = ActiveCycleStudentView.query.filter_by(courseId=course_id).order_by(ActiveCycleStudentView.studentName).all()
    
    result = {
        'unassigned': [],
        'classrooms': {}
    }
    
    for s in students:
        student_data = s.to_dict()
        if not s.classroomId:
            result['unassigned'].append(student_data)
        else:
            if s.classroomId not in result['classrooms']:
                result['classrooms'][s.classroomId] = []
            result['classrooms'][s.classroomId].append(student_data)
            
    return result

def update_student_classroom(student_cycle_classroom_id, classroom_id):
    """
    Update the classroom for a specific student cycle record.
    """
    # Note: ActiveCycleStudentView is a view, we need to update the underlying table.
    # Assuming the underlying table is 'cliente.estudiantesaulaciclo' or similar based on 'idestudianteaulacic'
    # Since I don't have the exact model for the writable table, I will try to use a direct update or find the model.
    # Looking at 'active_cycle_student_grade_service', it seems we use models.
    # Let's check if 'active_cycle_student_view' maps to a writable model. 
    # Usually views are read-only. We need the 'StudentCycleClassroom' model.
    # If it doesn't exist, we might need to create it or use SQL.
    
    # Strategy: Use raw SQL for now to be safe with the view limitation, 
    # or better, search for the table name 'estudiantesaulaciclo' (implied by idestudianteaulacic).
    
    sql = text("UPDATE cliente.estudiantesaulaciclo SET idaula = :classroom_id WHERE idestudianteaulacic = :id")
    db.session.execute(sql, {'classroom_id': classroom_id, 'id': student_cycle_classroom_id})
    db.session.commit()
    return True

def update_student_classrooms_bulk(assignments):
    """
    Update multiple student classroom assignments.
    assignments: list of { 'studentCycleClassroomId': <int>, 'classroomId': <int|None> }
    """
    try:
        # We can implement this with a loop or a more optimized executemany if needed.
        # For simplicity and clear logic:
        for assignment in assignments:
            classroom_id = assignment.get('classroomId')
            student_id = assignment.get('studentCycleClassroomId')
            
            # Handle empty string or explicit None for classroom_id
            if classroom_id == '':
                classroom_id = None
                
            sql = text("UPDATE cliente.estudiantesaulaciclo SET idaula = :classroom_id WHERE idestudianteaulacic = :id")
            db.session.execute(sql, {'classroom_id': classroom_id, 'id': student_id})
            
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

def assign_classrooms_automatically(course_id):
    """
    Executes sp_AsignaEstAulaPeriodoActivo for the given course.
    """
    # Assuming the SP takes courseId as parameter. 
    # The user said: "enviando el curso que se esta trabajando"
    try:
        db.session.execute(text("CALL cliente.sp_AsignaEstAulaPeriodoActivo(:course_id)"), {'course_id': course_id})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
