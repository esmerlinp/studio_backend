from app.models.client_scheme.payment_frequency_list_view import PaymentFrequencyListView

def get_payment_frequencies(filters=None):
    """
    Retrieve payment frequencies.
    """
    query = PaymentFrequencyListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(PaymentFrequencyListView.frequencyName).all()
