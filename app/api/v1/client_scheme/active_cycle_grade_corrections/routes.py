from flask import Blueprint
from . import controller

active_cycle_grade_corrections_bp = Blueprint('active_cycle_grade_corrections', __name__, url_prefix='/api/v1/client/active-cycle-grade-corrections')

active_cycle_grade_corrections_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
