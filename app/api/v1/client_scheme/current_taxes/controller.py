from flask import jsonify
from flask_jwt_extended import jwt_required
from app.services.client_scheme.current_tax_service import get_current_tax

@jwt_required()
def get_one():
    """
    Get the current active tax.
    """
    tax = get_current_tax()
    if not tax:
        return jsonify(None), 200
        
    return jsonify(tax.to_dict()), 200
