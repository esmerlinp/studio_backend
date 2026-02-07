from app.models.client_scheme.cycle_list_view import CycleListView
from sqlalchemy import desc

def get_cycles(filters=None):
    """
    Retrieve cycles.
    """
    query = CycleListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(desc(CycleListView.startDate)).all()
