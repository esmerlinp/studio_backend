from flask import Blueprint
from . import controller

schedule_block_details_bp = Blueprint('schedule_block_details', __name__, url_prefix='/api/v1/client/schedule-block-details')

schedule_block_details_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
