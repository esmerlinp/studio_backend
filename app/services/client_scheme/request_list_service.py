from app.models.client_scheme.request_list_view import RequestListView

def get_requests(filters=None):
    """
    Retrieve requests with support for filtering, search, and sorting.
    """
    query = RequestListView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('evaluationState'):
            query = query.filter_by(evaluationState=filters['evaluationState'])
            
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(RequestListView.applicantName.ilike(search_term))
            
        if filters.get('onlyPending'):
            # Assuming 'PENDIENTE' is a state or based on isInscribed
            # We use requestProcessState or evaluationState
            query = query.filter(RequestListView.isInscribed == False)
            
    return query.order_by(RequestListView.id.desc())
