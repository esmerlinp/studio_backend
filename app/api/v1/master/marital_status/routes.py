from flask import Blueprint
from . import controller

marital_status_bp = Blueprint('marital_status', __name__, url_prefix='/api/v1/master/marital-status')

marital_status_bp.get("/")(controller.get_marital_statuses)
marital_status_bp.get("/<int:status_id>")(controller.get_marital_status)
marital_status_bp.post("/")(controller.create_marital_status)
marital_status_bp.put("/<int:status_id>")(controller.update_marital_status)
marital_status_bp.delete("/<int:status_id>")(controller.delete_marital_status)
