from flask import Blueprint
from . import controller

subject_areas_bp = Blueprint('subject_areas', __name__, url_prefix='/api/v1/client/subject-areas')

subject_areas_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
