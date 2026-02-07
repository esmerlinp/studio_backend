from flask import Blueprint
from . import controller

health_insurance_institutions_bp = Blueprint('health_insurance_institutions', __name__, url_prefix='/api/v1/master/health-insurance-institutions')

health_insurance_institutions_bp.get("/")(controller.get_health_insurance_institutions)
health_insurance_institutions_bp.get("/<int:inst_id>")(controller.get_health_insurance_institution)
health_insurance_institutions_bp.post("/")(controller.create_health_insurance_institution)
health_insurance_institutions_bp.put("/<int:inst_id>")(controller.update_health_insurance_institution)
health_insurance_institutions_bp.delete("/<int:inst_id>")(controller.delete_health_insurance_institution)
