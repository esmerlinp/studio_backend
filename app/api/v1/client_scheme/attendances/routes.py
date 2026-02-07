from flask import Blueprint
from . import controller

attendances_bp = Blueprint('attendances', __name__, url_prefix='/api/v1/client/attendances')

attendances_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
attendances_bp.add_url_rule('/checklist', view_func=controller.get_checklist, methods=['GET'])
attendances_bp.add_url_rule('/bulk', view_func=controller.bulk_save, methods=['POST'])
