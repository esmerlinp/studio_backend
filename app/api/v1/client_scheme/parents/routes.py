from flask import Blueprint
from .controller import dashboard_view, student_360_view
from app import require_permission
from flask_jwt_extended import jwt_required

parents_bp = Blueprint('parents', __name__)

# Views
parents_bp.route('/', methods=['GET'])(jwt_required()(require_permission("SC_PADRES_DASHBOARD", "CONSULTAR")(dashboard_view)))
parents_bp.route('/student/<int:student_id>', methods=['GET'])(jwt_required()(require_permission("SC_PADRES_STUDENT_360", "CONSULTAR")(student_360_view)))
