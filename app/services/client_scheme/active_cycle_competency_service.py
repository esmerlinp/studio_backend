from app.models.client_scheme.active_cycle_competency_view import ActiveCycleCompetencyView

def get_active_cycle_competencies():
    """
    Retrieve all records from the active cycle competency view.
    """
    return ActiveCycleCompetencyView.query.all()

def get_active_cycle_competencies_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    filters: dict containing potential filter keys:
        - courseId
        - subCycleId
    """
    query = ActiveCycleCompetencyView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('subCycleId'):
            query = query.filter_by(subCycleId=filters['subCycleId'])
            
    return query.all()
