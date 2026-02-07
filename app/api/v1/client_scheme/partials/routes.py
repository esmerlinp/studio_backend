from flask import Blueprint
from . import controller

partials_bp = Blueprint('partials_list', __name__, url_prefix='/api/v1/client/partials-list')

partials_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
