from flask import Blueprint
from . import controller

grade_corrections_bp = Blueprint('grade_corrections_list', __name__, url_prefix='/api/v1/client/grade-corrections-list')

grade_corrections_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
