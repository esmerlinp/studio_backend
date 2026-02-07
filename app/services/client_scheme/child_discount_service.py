from app.models.client_scheme.child_discount_view import ChildDiscountView

def get_child_discounts(filters=None):
    """
    Retrieve child discounts.
    """
    query = ChildDiscountView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
    return query.order_by(ChildDiscountView.childNumber).all()
