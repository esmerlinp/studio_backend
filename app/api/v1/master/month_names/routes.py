from flask import Blueprint
from . import controller

month_names_bp = Blueprint('month_names', __name__)

month_names_bp.add_url_rule('/month-names', view_func=controller.get_months, methods=['GET'])
month_names_bp.add_url_rule('/month-names/<int:month_id>', view_func=controller.get_month, methods=['GET'])
month_names_bp.add_url_rule('/month-names', view_func=controller.create_month, methods=['POST'])
month_names_bp.add_url_rule('/month-names/<int:month_id>', view_func=controller.update_month, methods=['PUT'])
month_names_bp.add_url_rule('/month-names/<int:month_id>', view_func=controller.delete_month, methods=['DELETE'])
