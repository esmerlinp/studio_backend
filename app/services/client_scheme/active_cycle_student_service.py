from app.models.client_scheme.active_cycle_student_view import ActiveCycleStudentView

def get_active_cycle_students():
    """
    Retrieve all active cycle students.
    """
    return ActiveCycleStudentView.query.order_by(ActiveCycleStudentView.studentName).all()

def get_active_cycle_students_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    filters: dict containing potential filter keys:
        - studentId
        - courseId
        - levelId
        - cycleId
    """
    query = ActiveCycleStudentView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('levelId'):
            query = query.filter_by(levelId=filters['levelId'])
            
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
    return query.order_by(ActiveCycleStudentView.studentName).all()
