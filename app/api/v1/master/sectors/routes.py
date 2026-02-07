from flask import Blueprint
from . import controller

sectors_bp = Blueprint('sectors', __name__, url_prefix='/api/v1/master/sectors')

sectors_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
sectors_bp.add_url_rule('/<int:sector_id>', view_func=controller.get_one, methods=['GET'])
sectors_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
sectors_bp.add_url_rule('/<int:sector_id>', view_func=controller.update, methods=['PUT'])
sectors_bp.add_url_rule('/<int:sector_id>', view_func=controller.delete, methods=['DELETE'])
