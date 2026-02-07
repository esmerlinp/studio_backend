from app.models.client_scheme.inscription_list_view import InscriptionListView

def get_inscriptions(filters=None):
    """
    Retrieve inscriptions.
    """
    query = InscriptionListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('courseId'):
            query = query.filter_by(courseId=filters['courseId'])
            
    return query.order_by(InscriptionListView.studentName).all()
