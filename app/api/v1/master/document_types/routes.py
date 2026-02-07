from flask import Blueprint
from . import controller

document_types_bp = Blueprint('document_types', __name__, url_prefix='/api/v1/master/document-types')

document_types_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
document_types_bp.add_url_rule('/<int:dt_id>', view_func=controller.get_one, methods=['GET'])
document_types_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
document_types_bp.add_url_rule('/<int:dt_id>', view_func=controller.update, methods=['PUT'])
document_types_bp.add_url_rule('/<int:dt_id>', view_func=controller.delete, methods=['DELETE'])
