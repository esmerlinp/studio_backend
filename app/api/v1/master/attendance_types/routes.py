from flask import Blueprint
from . import controller

attendance_types_bp = Blueprint('attendance_types', __name__, url_prefix='/api/v1/master/attendance-types')

attendance_types_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
attendance_types_bp.add_url_rule('/<int:at_id>', view_func=controller.get_one, methods=['GET'])
attendance_types_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
attendance_types_bp.add_url_rule('/<int:at_id>', view_func=controller.update, methods=['PUT'])
attendance_types_bp.add_url_rule('/<int:at_id>', view_func=controller.delete, methods=['DELETE'])
