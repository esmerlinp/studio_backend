from app.models.client_scheme.student_list_view import StudentListView

def get_students(filters=None):
    """
    Retrieve students.
    """
    query = StudentListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('levelId'):
            query = query.filter_by(levelId=filters['levelId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('studentStateId'):
            query = query.filter_by(studentStateId=filters['studentStateId'])
            
    return query.order_by(StudentListView.fullName).all()

def get_student_by_id(student_id):
    """
    Retrieve a student by ID.
    """
    return StudentListView.query.filter_by(id=student_id).first()
