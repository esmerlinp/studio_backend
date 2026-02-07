from flask import Blueprint
from . import controller

currencies_bp = Blueprint('currencies', __name__)

currencies_bp.add_url_rule('/currencies', view_func=controller.get_currencies, methods=['GET'])
currencies_bp.add_url_rule('/currencies/<int:currency_id>', view_func=controller.get_currency, methods=['GET'])
currencies_bp.add_url_rule('/currencies', view_func=controller.create_currency, methods=['POST'])
currencies_bp.add_url_rule('/currencies/<int:currency_id>', view_func=controller.update_currency, methods=['PUT'])
currencies_bp.add_url_rule('/currencies/<int:currency_id>', view_func=controller.delete_currency, methods=['DELETE'])
