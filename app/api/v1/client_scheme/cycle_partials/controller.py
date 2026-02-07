from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.cycle_partial_list_service import get_cycle_partials

@jwt_required()
def get_all():
    """
    Get all cycle partials.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)
        
    data = get_cycle_partials(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
