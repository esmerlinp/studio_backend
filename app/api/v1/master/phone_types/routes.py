from flask import Blueprint
from . import controller

phone_types_bp = Blueprint('phone_types', __name__, url_prefix='/api/v1/master/phone-types')

phone_types_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
phone_types_bp.add_url_rule('/<int:pt_id>', view_func=controller.get_one, methods=['GET'])
phone_types_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
phone_types_bp.add_url_rule('/<int:pt_id>', view_func=controller.update, methods=['PUT'])
phone_types_bp.add_url_rule('/<int:pt_id>', view_func=controller.delete, methods=['DELETE'])
