from flask import Blueprint
from . import controller

payment_frequencies_bp = Blueprint('payment_frequencies_list', __name__, url_prefix='/api/v1/client/payment-frequencies-list')

payment_frequencies_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
