from app.models.client_scheme.course_list_view import CourseListView

def get_courses(filters=None):
    """
    Retrieve courses.
    """
    query = CourseListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
        if filters.get('levelId'):
             query = query.filter_by(levelId=filters['levelId'])

    return query.order_by(CourseListView.ordering).all()
