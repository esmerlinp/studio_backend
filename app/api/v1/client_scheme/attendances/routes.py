from flask import Blueprint
from . import controller

attendances_bp = Blueprint('attendances', __name__, url_prefix='/api/v1/client/attendances')

attendances_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
