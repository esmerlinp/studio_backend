from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.inscription_list_service import get_inscriptions

@jwt_required()
def get_all():
    """
    Get all inscriptions.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = get_inscriptions(filters)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
    return jsonify({
        "items": [item.to_dict() for item in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page
    }), 200
