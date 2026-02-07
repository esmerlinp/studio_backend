from app.models.client_scheme.tax_list_view import TaxListView

def get_taxes(filters=None):
    """
    Retrieve taxes.
    """
    query = TaxListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(TaxListView.date.desc()).all()
