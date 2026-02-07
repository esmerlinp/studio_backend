from flask import Blueprint
from . import controller

payment_calendar_bp = Blueprint('payment_calendar', __name__, url_prefix='/api/v1/client/payment-calendar')

payment_calendar_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
