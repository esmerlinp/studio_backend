from flask import Blueprint
from . import controller

current_taxes_bp = Blueprint('current_taxes', __name__, url_prefix='/api/v1/client/current-taxes')

current_taxes_bp.add_url_rule('/', view_func=controller.get_one, methods=['GET'])
