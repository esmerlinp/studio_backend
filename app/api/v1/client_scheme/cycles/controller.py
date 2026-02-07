from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.cycle_list_service import get_cycles

@jwt_required()
def get_all():
    """
    Get all cycles.
    """
    filters = {}
    if request.args.get('isActive') is not None:
        filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
    data = get_cycles(filters)
        
    return jsonify([item.to_dict() for item in data]), 200

@jwt_required()
def activate(cycle_id):
    """
    Activate a cycle.
    """
    from app.services.client_scheme.cycle_list_service import activate_cycle
    from app.utils.responses import success, error
    
    try:
        activate_cycle(cycle_id)
        return success({}, "Cycle activated successfully")
    except ValueError as e:
        return error(str(e), 404)
    except Exception as e:
        return error(str(e), 500)
