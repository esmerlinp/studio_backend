from flask import Blueprint
from . import controller

active_cycle_attendances_bp = Blueprint('active_cycle_attendances', __name__, url_prefix='/api/v1/client/active-cycle-attendances')

active_cycle_attendances_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
