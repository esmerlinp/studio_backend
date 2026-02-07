from app.models.client_scheme.partial_list_view import PartialListView

def get_partials(filters=None):
    """
    Retrieve partials.
    """
    query = PartialListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(PartialListView.name).all()
