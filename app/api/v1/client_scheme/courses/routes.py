from flask import Blueprint
from . import controller

courses_bp = Blueprint('courses_list', __name__, url_prefix='/api/v1/client/courses-list')

courses_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
