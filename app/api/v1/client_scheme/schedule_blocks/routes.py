from flask import Blueprint
from . import controller

schedule_blocks_bp = Blueprint('schedule_blocks', __name__, url_prefix='/api/v1/client/schedule-blocks')

schedule_blocks_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
