from flask import Blueprint
from . import controller

medical_institutions_bp = Blueprint('medical_institutions', __name__, url_prefix='/api/v1/master/medical-institutions')

medical_institutions_bp.get("/")(controller.get_medical_institutions)
medical_institutions_bp.get("/<int:inst_id>")(controller.get_medical_institution)
medical_institutions_bp.post("/")(controller.create_medical_institution)
medical_institutions_bp.put("/<int:inst_id>")(controller.update_medical_institution)
medical_institutions_bp.delete("/<int:inst_id>")(controller.delete_medical_institution)
