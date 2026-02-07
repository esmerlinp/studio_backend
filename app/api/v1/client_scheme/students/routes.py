from flask import Blueprint
from . import controller

students_bp = Blueprint('students_list', __name__, url_prefix='/api/v1/client/students-list')

students_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
students_bp.add_url_rule('/<int:id>', view_func=controller.get_by_id, methods=['GET'])
students_bp.add_url_rule('/', view_func=controller.save, methods=['POST'])
students_bp.add_url_rule('/<int:id>', view_func=controller.save, methods=['PUT'])
