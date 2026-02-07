from flask import Blueprint
from . import controller

child_discounts_bp = Blueprint('child_discounts', __name__, url_prefix='/api/v1/client/child-discounts')

child_discounts_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
