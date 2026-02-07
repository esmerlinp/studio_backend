from flask import Blueprint
from . import controller

modules_bp = Blueprint('modules', __name__)

modules_bp.add_url_rule('/modules', view_func=controller.get_modules, methods=['GET'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.get_module, methods=['GET'])
modules_bp.add_url_rule('/modules', view_func=controller.create_module, methods=['POST'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.update_module, methods=['PUT'])
modules_bp.add_url_rule('/modules/<int:module_id>', view_func=controller.delete_module, methods=['DELETE'])
