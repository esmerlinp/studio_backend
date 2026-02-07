from flask import Blueprint
from . import controller

active_cycle_students_bp = Blueprint('active_cycle_students', __name__, url_prefix='/api/v1/client/active-cycle-students')

active_cycle_students_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
