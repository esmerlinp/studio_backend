from app.models.client_scheme.classroom_model import Classroom

def get_classrooms(course_id=None):
    """
    Retrieve classrooms, optionally filtered by courseId.
    """
    query = Classroom.query
    
    if course_id:
        query = query.filter_by(courseId=course_id)
        
    return query.all()
