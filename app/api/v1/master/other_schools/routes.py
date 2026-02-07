from flask import Blueprint
from . import controller

other_schools_bp = Blueprint('other_schools', __name__)

other_schools_bp.add_url_rule('/other-schools', view_func=controller.get_other_schools, methods=['GET'])
other_schools_bp.add_url_rule('/other-schools/<int:school_id>', view_func=controller.get_other_school, methods=['GET'])
other_schools_bp.add_url_rule('/other-schools', view_func=controller.create_other_school, methods=['POST'])
other_schools_bp.add_url_rule('/other-schools/<int:school_id>', view_func=controller.update_other_school, methods=['PUT'])
other_schools_bp.add_url_rule('/other-schools/<int:school_id>', view_func=controller.delete_other_school, methods=['DELETE'])
