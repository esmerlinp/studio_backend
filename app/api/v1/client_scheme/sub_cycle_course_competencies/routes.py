from flask import Blueprint
from . import controller

sub_cycle_course_competencies_bp = Blueprint('sub_cycle_course_competencies', __name__, url_prefix='/api/v1/client/sub-cycle-course-competencies')

sub_cycle_course_competencies_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
