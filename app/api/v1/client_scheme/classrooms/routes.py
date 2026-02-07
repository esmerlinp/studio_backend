from flask import Blueprint
from . import controller

classrooms_bp = Blueprint('classrooms', __name__, url_prefix='/api/v1/client/classrooms')

classrooms_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
