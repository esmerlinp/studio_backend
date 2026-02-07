from app.models.client_scheme.cycle_partial_list_view import CyclePartialListView

def get_cycle_partials(filters=None):
    """
    Retrieve cycle partials.
    """
    query = CyclePartialListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('levelId'):
            query = query.filter_by(levelId=filters['levelId'])
            
    return query.order_by(CyclePartialListView.partialName).all()
