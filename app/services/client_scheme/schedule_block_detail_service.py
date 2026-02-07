from app.models.client_scheme.schedule_block_detail_view import ScheduleBlockDetailView

def get_schedule_block_details():
    """
    Retrieve all schedule block details.
    """
    return ScheduleBlockDetailView.query.order_by(
        ScheduleBlockDetailView.scheduleBlockId,
        ScheduleBlockDetailView.startTime
    ).all()

def get_schedule_block_details_filtered(filters=None):
    """
    Retrieve records filtered by various criteria.
    filters: dict containing potential filter keys:
        - scheduleBlockId
        - isActive
    """
    query = ScheduleBlockDetailView.query
    
    if filters:
        if filters.get('scheduleBlockId'):
            query = query.filter_by(scheduleBlockId=filters['scheduleBlockId'])
            
        if 'isActive' in filters:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(
        ScheduleBlockDetailView.scheduleBlockId,
        ScheduleBlockDetailView.startTime
    ).all()
