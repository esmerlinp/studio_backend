from flask import Blueprint
from . import controller

inscriptions_bp = Blueprint('inscriptions_list', __name__, url_prefix='/api/v1/client/inscriptions-list')

inscriptions_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
