from app.models.client_scheme.schedule_block_list_view import ScheduleBlockListView

def get_schedule_blocks(filters=None):
    """
    Retrieve schedule blocks.
    """
    query = ScheduleBlockListView.query
    
    if filters:
        if filters.get('isActive') is not None:
             query = query.filter_by(isActive=filters['isActive'])
            
    return query.order_by(ScheduleBlockListView.name).all()
