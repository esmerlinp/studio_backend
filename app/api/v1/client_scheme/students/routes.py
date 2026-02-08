from flask import Blueprint
from . import controller

students_bp = Blueprint('students_list', __name__, url_prefix='/api/v1/client/students-list')

students_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
students_bp.add_url_rule('/<int:id>', view_func=controller.get_by_id, methods=['GET'])
students_bp.add_url_rule('/', view_func=controller.save, methods=['POST'])
students_bp.add_url_rule('/<int:id>', view_func=controller.save, methods=['PUT'])

# Document management routes
students_bp.add_url_rule('/<int:student_id>/documents', view_func=controller.get_student_documents, methods=['GET'])
students_bp.add_url_rule('/<int:student_id>/documents', view_func=controller.upload_student_document, methods=['POST'])
students_bp.add_url_rule('/<int:student_id>/documents/<int:document_id>', view_func=controller.get_student_document, methods=['GET'])
students_bp.add_url_rule('/<int:student_id>/documents/<int:document_id>', view_func=controller.delete_student_document, methods=['DELETE'])
