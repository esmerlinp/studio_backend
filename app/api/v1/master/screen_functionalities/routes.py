from flask import Blueprint
from . import controller

screen_functionalities_bp = Blueprint('screen_functionalities', __name__, url_prefix='/api/v1/master/screen-functionalities')

screen_functionalities_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
screen_functionalities_bp.add_url_rule('/<int:sf_id>', view_func=controller.get_one, methods=['GET'])
screen_functionalities_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
screen_functionalities_bp.add_url_rule('/<int:sf_id>', view_func=controller.update, methods=['PUT'])
screen_functionalities_bp.add_url_rule('/<int:sf_id>', view_func=controller.delete, methods=['DELETE'])
