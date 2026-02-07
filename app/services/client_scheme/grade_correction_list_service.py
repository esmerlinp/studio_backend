from app.models.client_scheme.grade_correction_list_view import GradeCorrectionListView

def get_grade_corrections(filters=None):
    """
    Retrieve grade corrections.
    """
    query = GradeCorrectionListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
    return query.order_by(GradeCorrectionListView.changeDate.desc()).all()
