from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services.client_scheme.classroom_service import get_classrooms

@jwt_required()
def get_all():
    """
    Get all classrooms, optionally filtering by courseId.
    """
    course_id = request.args.get('courseId', type=int)
    data = get_classrooms(course_id)
    return jsonify([item.to_dict() for item in data]), 200
