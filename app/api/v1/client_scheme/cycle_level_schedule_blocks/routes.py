from flask import Blueprint
from . import controller

cycle_level_schedule_blocks_bp = Blueprint('cycle_level_schedule_blocks', __name__, url_prefix='/api/v1/client/cycle-level-schedule-blocks')

cycle_level_schedule_blocks_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
