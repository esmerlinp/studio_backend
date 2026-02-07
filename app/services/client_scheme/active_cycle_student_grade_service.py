from app.models.client_scheme.active_cycle_student_grade_view import ActiveCycleStudentGradeView

def get_active_cycle_student_grades(filters=None):
    """
    Retrieve active cycle student grades.
    """
    query = ActiveCycleStudentGradeView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('subjectId'):
            query = query.filter_by(subjectId=filters['subjectId'])
            
    return query.order_by(ActiveCycleStudentGradeView.studentName).all()

def get_grades_checklist(filters):
    """
    Retrieve students and their grade for a specific subject and partial.
    filters: 
        - courseId (required)
        - subjectId (required)
        - partialId (required)
        - classroomId (optional)
        - cycleId (required)
    """
    from app.services.client_scheme.active_cycle_student_service import get_active_cycle_students_filtered
    from app.models.client_scheme.grade_model import Grade
    
    # 1. Fetch Students
    student_filters = {
        'cycleId': filters.get('cycleId'),
        'courseId': filters.get('courseId'),
        'classroomId': filters.get('classroomId')
    }
    students_query = get_active_cycle_students_filtered(student_filters)
    students = students_query.all()
    
    if not students:
        return []
        
    student_ids = [s.studentCycleClassroomId for s in students]
    
    # 2. Fetch Existing Grades
    grades_query = Grade.query.filter(
        Grade.studentCycleClassroomId.in_(student_ids),
        Grade.partialId == filters['partialId'],
        Grade.subjectId == filters['subjectId']
    )
    existing_grades = {g.studentCycleClassroomId: g for g in grades_query.all()}
    
    # 3. Map Data
    checklist = []
    for s in students:
        grade_record = existing_grades.get(s.studentCycleClassroomId)
        checklist.append({
            "studentCycleClassroomId": s.studentCycleClassroomId,
            "studentCode": s.studentCode,
            "studentName": s.studentName,
            "gradeId": grade_record.id if grade_record else None,
            "grade": float(grade_record.grade) if grade_record and grade_record.grade is not None else None
        })
        
    return checklist

def save_grades(data):
    """
    Save or update multiple grade records.
    data: list of dicts {studentCycleClassroomId, subjectId, partialId, grade}
    """
    from app.models.client_scheme.grade_model import Grade
    from app import db
    
    results = []
    for item in data:
        student_cycle_classroom_id = item.get('studentCycleClassroomId')
        subject_id = item.get('subjectId')
        partial_id = item.get('partialId')
        grade_value = item.get('grade')
        
        if not all([student_cycle_classroom_id, subject_id, partial_id]):
            continue
            
        # Check if record exists
        grade_record = Grade.query.filter_by(
            studentCycleClassroomId=student_cycle_classroom_id,
            subjectId=subject_id,
            partialId=partial_id
        ).first()
        
        if grade_record:
            # Update
            if grade_value is None or grade_value == '':
                 # Option: Delete if empty? Or set to null. Let's set to null for now or keep previous if not provided?
                 # If explicit null is sent, update.
                 grade_record.grade = None
            else:
                 grade_record.grade = grade_value
        else:
            # Create
            if grade_value is not None and grade_value != '':
                grade_record = Grade(
                    studentCycleClassroomId=student_cycle_classroom_id,
                    subjectId=subject_id,
                    partialId=partial_id,
                    grade=grade_value
                )
                db.session.add(grade_record)
            
        if grade_record:
            results.append(grade_record)
        
    db.session.commit()
    return results
