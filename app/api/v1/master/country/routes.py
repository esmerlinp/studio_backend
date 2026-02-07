from flask import Blueprint
from . import controller

country_bp = Blueprint('country', __name__)

country_bp.add_url_rule('/countries', view_func=controller.get_countries, methods=['GET'])
country_bp.add_url_rule('/countries/<int:country_id>', view_func=controller.get_country, methods=['GET'])
country_bp.add_url_rule('/countries', view_func=controller.create_country, methods=['POST'])
country_bp.add_url_rule('/countries/<int:country_id>', view_func=controller.update_country, methods=['PUT'])
country_bp.add_url_rule('/countries/<int:country_id>', view_func=controller.delete_country, methods=['DELETE'])
