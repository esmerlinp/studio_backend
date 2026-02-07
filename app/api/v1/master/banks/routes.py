from flask import Blueprint
from . import controller

banks_bp = Blueprint('banks', __name__, url_prefix='/api/v1/master/banks')

banks_bp.get("/")(controller.get_banks)
banks_bp.get("/<int:bank_id>")(controller.get_bank)
banks_bp.post("/")(controller.create_bank)
banks_bp.put("/<int:bank_id>")(controller.update_bank)
banks_bp.delete("/<int:bank_id>")(controller.delete_bank)
