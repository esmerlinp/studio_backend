from flask import Blueprint
from . import controller

competencies_bp = Blueprint('competencies_list', __name__, url_prefix='/api/v1/client/competencies-list')

competencies_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
