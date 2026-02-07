from app.models.client_scheme.subject_area_list_view import SubjectAreaListView

def get_subject_areas(filters=None):
    """
    Retrieve subject areas.
    """
    query = SubjectAreaListView.query
    
    if filters:
        if filters.get('isActive') is not None:
            query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(SubjectAreaListView.name).all()
