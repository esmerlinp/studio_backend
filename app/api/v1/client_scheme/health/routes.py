from flask import Blueprint
from .controller import get_health_profile, log_visit, save_authorization

health_api_bp = Blueprint('health_api', __name__)

health_api_bp.route('/student/<int:student_id>/profile', methods=['GET'])(get_health_profile)
health_api_bp.route('/visit', methods=['POST'])(log_visit)
health_api_bp.route('/authorization', methods=['POST'])(save_authorization)
