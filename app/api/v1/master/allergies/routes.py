from flask import Blueprint
from . import controller

allergies_bp = Blueprint('allergies', __name__, url_prefix='/api/v1/master/allergies')

allergies_bp.get("/")(controller.get_allergies)
allergies_bp.get("/<int:allergy_id>")(controller.get_allergy)
allergies_bp.post("/")(controller.create_allergy)
allergies_bp.put("/<int:allergy_id>")(controller.update_allergy)
allergies_bp.delete("/<int:allergy_id>")(controller.delete_allergy)
