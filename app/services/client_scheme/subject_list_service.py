from app.models.client_scheme.subject_list_view import SubjectListView

def get_subjects(filters=None):
    """
    Retrieve subjects.
    """
    query = SubjectListView.query
    
    if filters:
        if filters.get('subjectAreaId'):
            query = query.filter_by(subjectAreaId=filters['subjectAreaId'])

        if filters.get('isActive') is not None:
            query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(SubjectListView.ordering).all()
