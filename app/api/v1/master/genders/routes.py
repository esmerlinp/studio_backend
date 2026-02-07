from flask import Blueprint
from . import controller

genders_bp = Blueprint('genders', __name__, url_prefix='/api/v1/master/genders')

genders_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
genders_bp.add_url_rule('/<int:gender_id>', view_func=controller.get_one, methods=['GET'])
genders_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
genders_bp.add_url_rule('/<int:gender_id>', view_func=controller.update, methods=['PUT'])
genders_bp.add_url_rule('/<int:gender_id>', view_func=controller.delete, methods=['DELETE'])
