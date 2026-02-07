from app.models.client_scheme.competency_list_view import CompetencyListView

def get_competencies(filters=None):
    """
    Retrieve competencies.
    """
    query = CompetencyListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(CompetencyListView.ordering).all()
