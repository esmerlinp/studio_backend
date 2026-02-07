from flask import Blueprint
from . import controller

levels_bp = Blueprint('levels_list', __name__, url_prefix='/api/v1/client/levels-list')

levels_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
