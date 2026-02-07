from app.models.client_scheme.attendance_list_view import AttendanceListView
from sqlalchemy import desc

def get_attendances(filters=None):
    """
    Retrieve attendances.
    """
    query = AttendanceListView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('date'):
            query = query.filter_by(date=filters['date'])
            
    return query.order_by(desc(AttendanceListView.date)).all()
