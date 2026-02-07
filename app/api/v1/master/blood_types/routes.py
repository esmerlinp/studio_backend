from flask import Blueprint
from . import controller

blood_types_bp = Blueprint('blood_types', __name__, url_prefix='/api/v1/master/blood-types')

blood_types_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
blood_types_bp.add_url_rule('/<int:bt_id>', view_func=controller.get_one, methods=['GET'])
blood_types_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
blood_types_bp.add_url_rule('/<int:bt_id>', view_func=controller.update, methods=['PUT'])
blood_types_bp.add_url_rule('/<int:bt_id>', view_func=controller.delete, methods=['DELETE'])
