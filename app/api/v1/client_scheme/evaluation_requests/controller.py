from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.evaluation_request_list_service import get_evaluation_requests

@jwt_required()
def get_all():
    """
    Get all evaluation requests.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('evaluationState'):
        filters['evaluationState'] = request.args.get('evaluationState', type=int)
        
    data = get_evaluation_requests(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
