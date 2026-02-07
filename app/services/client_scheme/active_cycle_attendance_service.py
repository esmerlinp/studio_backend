from app.models.client_scheme.active_cycle_attendance_view import ActiveCycleAttendanceView
from sqlalchemy import desc

def get_active_cycle_attendances(limit=None):
    """
    Retrieve all records from the active cycle attendance view.
    Orders results by date descending.
    """
    query = ActiveCycleAttendanceView.query.order_by(desc(ActiveCycleAttendanceView.date))
    
    if limit:
        query = query.limit(limit)
        
    return query.all()

def get_active_cycle_attendances_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    filters: dict containing potential filter keys:
        - studentId
        - date
        - courseId
        - attendanceTypeId
    """
    query = ActiveCycleAttendanceView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('date'):
            query = query.filter_by(date=filters['date'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('attendanceTypeId'):
            query = query.filter_by(attendanceTypeId=filters['attendanceTypeId'])
            
    return query.order_by(desc(ActiveCycleAttendanceView.date)).all()
