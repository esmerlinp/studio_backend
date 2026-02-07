from app.models.client_scheme.cycle_level_schedule_block_view import CycleLevelScheduleBlockView

def get_cycle_level_schedule_blocks(filters=None):
    """
    Retrieve cycle level schedule blocks.
    """
    query = CycleLevelScheduleBlockView.query
    
    if filters:
        if filters.get('cycleId'):
            query = query.filter_by(cycleId=filters['cycleId'])
            
        if filters.get('levelId'):
            query = query.filter_by(levelId=filters['levelId'])
            
    return query.order_by(CycleLevelScheduleBlockView.cycleName, CycleLevelScheduleBlockView.levelName).all()
