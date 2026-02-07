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
