from app.models.client_scheme.active_cycle_grade_correction_view import ActiveCycleGradeCorrectionView

def get_active_cycle_grade_corrections(filters=None):
    """
    Retrieve active cycle grade corrections.
    """
    query = ActiveCycleGradeCorrectionView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('teacherId'):
            query = query.filter_by(teacherId=filters['teacherId'])
            
    return query.order_by(ActiveCycleGradeCorrectionView.requestDate.desc()).all()
