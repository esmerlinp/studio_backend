from flask import Blueprint
from . import controller

cycle_partials_bp = Blueprint('cycle_partials_list', __name__, url_prefix='/api/v1/client/cycle-partials-list')

cycle_partials_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
