from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.schedule_block_detail_service import get_schedule_block_details_filtered

@jwt_required()
def get_all():
    """
    Get all schedule block details.
    Supports filtering by scheduleBlockId and isActive via query params.
    """
    filters = {}
    
    if request.args.get('scheduleBlockId'):
        filters['scheduleBlockId'] = request.args.get('scheduleBlockId', type=int)
        
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    data = get_schedule_block_details_filtered(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
