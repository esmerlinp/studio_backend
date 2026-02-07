from flask import Blueprint
from . import controller

active_cycle_competencies_bp = Blueprint('active_cycle_competencies', __name__, url_prefix='/api/v1/client/active-cycle-competencies')

active_cycle_competencies_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
