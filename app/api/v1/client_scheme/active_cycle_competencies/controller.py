from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.active_cycle_competency_service import get_active_cycle_competencies_filtered

@jwt_required()
def get_all():
    """
    Get all active cycle competencies.
    Supports filtering by courseId and subCycleId via query params.
    """
    filters = {}
    
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('subCycleId'):
        filters['subCycleId'] = request.args.get('subCycleId', type=int)
        
    data = get_active_cycle_competencies_filtered(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
