from app.models.client_scheme.school_payment_view import SchoolPaymentView

def get_school_payments(filters=None):
    """
    Retrieve school payments.
    """
    query = SchoolPaymentView.query
    
    if filters:
        if filters.get('studentId'):
            query = query.filter_by(studentId=filters['studentId'])
            
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
    return query.order_by(SchoolPaymentView.paymentDate.desc()).all()
