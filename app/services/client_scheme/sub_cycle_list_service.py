from app.models.client_scheme.sub_cycle_list_view import SubCycleListView

def get_sub_cycles(filters=None):
    """
    Retrieve sub cycles.
    """
    query = SubCycleListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('isCycleActive') is not None:
             query = query.filter_by(isCycleActive=filters['isCycleActive'])
            
    return query.order_by(SubCycleListView.order).all()
