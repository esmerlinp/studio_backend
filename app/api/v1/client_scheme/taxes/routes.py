from flask import Blueprint
from . import controller

taxes_bp = Blueprint('taxes_list', __name__, url_prefix='/api/v1/client/taxes-list')

taxes_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
