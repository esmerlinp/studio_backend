from flask import Blueprint
from app.api.v1.master.intelligence.controller import get_report

intelligence_bp = Blueprint('intelligence', __name__, url_prefix='/api/v1/intelligence')

intelligence_bp.post("/students/<int:student_id>/insights")(get_report)