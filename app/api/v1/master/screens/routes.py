from flask import Blueprint
from . import controller

screens_bp = Blueprint('screens', __name__, url_prefix='/api/v1/master/screens')

screens_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
screens_bp.add_url_rule('/<int:screen_id>', view_func=controller.get_one, methods=['GET'])
screens_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
screens_bp.add_url_rule('/<int:screen_id>', view_func=controller.update, methods=['PUT'])
screens_bp.add_url_rule('/<int:screen_id>', view_func=controller.delete, methods=['DELETE'])
