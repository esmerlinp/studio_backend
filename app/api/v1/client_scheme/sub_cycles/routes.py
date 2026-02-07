from flask import Blueprint
from . import controller

sub_cycles_bp = Blueprint('sub_cycles_list', __name__, url_prefix='/api/v1/client/sub-cycles-list')

sub_cycles_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
