from flask import Blueprint
from . import controller

cycles_bp = Blueprint('cycles', __name__, url_prefix='/api/v1/client/cycles')

cycles_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
cycles_bp.add_url_rule('/<int:cycle_id>/activate', view_func=controller.activate, methods=['PUT'])
