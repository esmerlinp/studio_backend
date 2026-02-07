from app.models.client_scheme.payment_calendar_list_view import PaymentCalendarListView

def get_payment_calendar(filters=None):
    """
    Retrieve payment calendar.
    """
    query = PaymentCalendarListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
    return query.order_by(PaymentCalendarListView.cycleId, PaymentCalendarListView.paymentFrequencyId, PaymentCalendarListView.quotaNumber).all()
