from flask import Blueprint
from . import controller

evaluation_requests_bp = Blueprint('evaluation_requests', __name__, url_prefix='/api/v1/client/evaluation-requests')

evaluation_requests_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
