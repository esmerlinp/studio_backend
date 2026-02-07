from app.models.client_scheme.surcharge_per_day_list_view import SurchargePerDayListView

def get_surcharges_per_day(filters=None):
    """
    Retrieve surcharges per day.
    """
    query = SurchargePerDayListView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
    return query.order_by(SurchargePerDayListView.days).all()
