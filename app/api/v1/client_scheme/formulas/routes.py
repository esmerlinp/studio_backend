from flask import Blueprint
from . import controller

formulas_bp = Blueprint('formulas_list', __name__, url_prefix='/api/v1/client/formulas-list')

formulas_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
