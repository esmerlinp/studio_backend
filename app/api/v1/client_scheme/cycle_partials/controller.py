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
        
    if filters.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)

    if request.args.get('subCycleId'):
        filters['subCycleId'] = request.args.get('subCycleId', type=int)
        
    data = get_cycle_partials(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
