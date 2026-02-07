from app.models.client_scheme.evaluation_request_list_view import EvaluationRequestListView

def get_evaluation_requests(filters=None):
    """
    Retrieve evaluation requests.
    """
    query = EvaluationRequestListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
        if filters.get('evaluationState'):
            query = query.filter_by(evaluationState=filters['evaluationState'])
            
    return query.order_by(EvaluationRequestListView.evaluationDate.desc()).all()
