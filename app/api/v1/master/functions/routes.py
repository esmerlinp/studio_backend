from flask import Blueprint
from . import controller

functions_bp = Blueprint('functions', __name__, url_prefix='/api/v1/master/functions')

functions_bp.get("/")(controller.get_functions)
functions_bp.get("/<int:func_id>")(controller.get_function)
functions_bp.post("/")(controller.create_function)
functions_bp.put("/<int:func_id>")(controller.update_function)
functions_bp.delete("/<int:func_id>")(controller.delete_function)
