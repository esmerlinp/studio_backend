from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.surcharge_per_day_list_service import get_surcharges_per_day

@jwt_required()
def get_all():
    """
    Get all surcharges per day.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    data = get_surcharges_per_day(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
