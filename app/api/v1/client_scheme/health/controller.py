from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.nursing_service import (
    create_nursing_visit, get_student_health_profile, add_medication_authorization
)

@jwt_required()
def get_health_profile(student_id):
    """Retrieve full health profile for a student."""
    profile = get_student_health_profile(student_id)
    return jsonify(profile)

@jwt_required()
def log_visit():
    """Create a nursing visit record."""
    data = request.get_json()
    visit_id, error_msg = create_nursing_visit(data)
    
    if error_msg:
        return jsonify({"error": error_msg}), 400
        
    return jsonify({
        "success": True, 
        "visitId": visit_id,
        "message": "Visita registrada y padres notificados."
    })

@jwt_required()
def save_authorization():
    """Register a new medication authorization."""
    data = request.get_json()
    auth_id = add_medication_authorization(data)
    return jsonify({"success": True, "authId": auth_id})
