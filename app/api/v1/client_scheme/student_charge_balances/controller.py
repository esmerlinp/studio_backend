from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.student_charge_balance_service import get_student_charge_balances_filtered

@jwt_required()
def get_all():
    """
    Get all student charge balances.
    Supports filtering by studentId, familyCode, cycleId, courseId, conceptId, and isFamily via query params.
    """
    filters = {}
    
    if request.args.get('studentId'):
        filters['studentId'] = request.args.get('studentId', type=int)
        
    if request.args.get('familyCode'):
        filters['familyCode'] = request.args.get('familyCode')
        
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('conceptId'):
        filters['conceptId'] = request.args.get('conceptId', type=int)
        
    if request.args.get('isFamily') is not None:
        filters['isFamily'] = request.args.get('isFamily').lower() == 'true'
        
    data = get_student_charge_balances_filtered(filters)
        
    return jsonify([item.to_dict() for item in data]), 200
