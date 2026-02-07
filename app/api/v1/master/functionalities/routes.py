from flask import Blueprint
from . import controller

functionalities_bp = Blueprint('functionalities', __name__, url_prefix='/api/v1/master/functionalities')

functionalities_bp.get("/")(controller.get_functionalities)
functionalities_bp.get("/<int:func_id>")(controller.get_functionality)
functionalities_bp.post("/")(controller.create_functionality)
functionalities_bp.put("/<int:func_id>")(controller.update_functionality)
functionalities_bp.delete("/<int:func_id>")(controller.delete_functionality)
