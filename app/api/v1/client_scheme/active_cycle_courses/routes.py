from flask import Blueprint
from . import controller

active_cycle_courses_bp = Blueprint('active_cycle_courses', __name__, url_prefix='/api/v1/client/active-cycle-courses')

active_cycle_courses_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
