from flask import Blueprint
from . import controller

surcharges_per_day_bp = Blueprint('surcharges_per_day_list', __name__, url_prefix='/api/v1/client/surcharges-per-day-list')

surcharges_per_day_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
