from app.models.client_scheme.request_list_view import RequestListView

def get_requests(filters=None):
    """
    Retrieve requests.
    """
    query = RequestListView.query
    
    if filters:
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('evaluationState'):
            query = query.filter_by(evaluationState=filters['evaluationState'])
            
    return query.order_by(RequestListView.applicantName).all()
