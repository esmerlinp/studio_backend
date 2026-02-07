from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.request_list_service import get_requests

@jwt_required()
def get_all():
    """
    Get all requests with pagination and filtering.
    """
    filters = {}
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('evaluationState'):
        filters['evaluationState'] = request.args.get('evaluationState', type=int)

    if request.args.get('search'):
        filters['search'] = request.args.get('search')
        
    if request.args.get('onlyPending'):
        filters['onlyPending'] = request.args.get('onlyPending') == 'true'
        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = get_requests(filters)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
    return jsonify({
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page
    }), 200
