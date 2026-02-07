from flask import Blueprint
from . import controller

payment_processors_bp = Blueprint('payment_processors', __name__, url_prefix='/api/v1/master/payment-processors')

payment_processors_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
payment_processors_bp.add_url_rule('/<int:pp_id>', view_func=controller.get_one, methods=['GET'])
payment_processors_bp.add_url_rule('/', view_func=controller.create, methods=['POST'])
payment_processors_bp.add_url_rule('/<int:pp_id>', view_func=controller.update, methods=['PUT'])
payment_processors_bp.add_url_rule('/<int:pp_id>', view_func=controller.delete, methods=['DELETE'])
