from flask import Blueprint
from . import controller

professions_bp = Blueprint('professions', __name__, url_prefix='/api/v1/master/professions')

professions_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
professions_bp.add_url_rule('/<int:profession_id>', view_func=controller.get_one, methods=['GET'])
professions_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
professions_bp.add_url_rule('/<int:profession_id>', view_func=controller.update, methods=['PUT'])
professions_bp.add_url_rule('/<int:profession_id>', view_func=controller.delete, methods=['DELETE'])
