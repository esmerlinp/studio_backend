from flask import Blueprint
from . import controller

concepts_bp = Blueprint('concepts_list', __name__, url_prefix='/api/v1/client/concepts-list')

concepts_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
