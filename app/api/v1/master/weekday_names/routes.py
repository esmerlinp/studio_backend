from flask import Blueprint
from . import controller

weekday_names_bp = Blueprint('weekday_names', __name__)

weekday_names_bp.add_url_rule('/weekday-names', view_func=controller.get_weekdays, methods=['GET'])
weekday_names_bp.add_url_rule('/weekday-names/<int:weekday_id>', view_func=controller.get_weekday, methods=['GET'])
weekday_names_bp.add_url_rule('/weekday-names', view_func=controller.create_weekday, methods=['POST'])
weekday_names_bp.add_url_rule('/weekday-names/<int:weekday_id>', view_func=controller.update_weekday, methods=['PUT'])
weekday_names_bp.add_url_rule('/weekday-names/<int:weekday_id>', view_func=controller.delete_weekday, methods=['DELETE'])
