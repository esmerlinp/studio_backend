from flask import Blueprint
from . import controller

subjects_bp = Blueprint('subjects', __name__, url_prefix='/api/v1/client/subjects')

subjects_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
