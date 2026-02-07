from app.models.client_scheme.level_list_view import LevelListView

def get_levels(filters=None):
    """
    Retrieve levels.
    """
    query = LevelListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(LevelListView.name).all()
