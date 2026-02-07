from flask import Blueprint
from . import controller

requests_bp = Blueprint('requests_list', __name__, url_prefix='/api/v1/client/requests-list')

requests_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
