from flask import Blueprint
from . import controller

active_cycle_student_grades_bp = Blueprint('active_cycle_student_grades', __name__, url_prefix='/api/v1/client/active-cycle-student-grades')

active_cycle_student_grades_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
active_cycle_student_grades_bp.add_url_rule('/checklist', view_func=controller.get_checklist, methods=['GET'])
active_cycle_student_grades_bp.add_url_rule('/bulk', view_func=controller.save_bulk, methods=['POST'])
