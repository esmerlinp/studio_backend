from flask import Blueprint
from . import controller

active_cycle_students_bp = Blueprint('active_cycle_students', __name__, url_prefix='/api/v1/client/active-cycle-students')

active_cycle_students_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
active_cycle_students_bp.add_url_rule('/assignment-board', view_func=controller.get_assignment_board, methods=['GET'])
active_cycle_students_bp.add_url_rule('/assign-classroom', view_func=controller.assign_classroom, methods=['POST'])
active_cycle_students_bp.add_url_rule('/bulk-assign-classrooms', view_func=controller.bulk_assign_classrooms, methods=['POST'])
active_cycle_students_bp.add_url_rule('/auto-assign', view_func=controller.auto_assign, methods=['POST'])
