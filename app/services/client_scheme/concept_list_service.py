from app.models.client_scheme.concept_list_view import ConceptListView

def get_concepts(filters=None):
    """
    Retrieve concepts.
    """
    query = ConceptListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
        if filters.get('isFamily') is not None:
             query = query.filter_by(isFamily=filters['isFamily'])

    return query.order_by(ConceptListView.name).all()
