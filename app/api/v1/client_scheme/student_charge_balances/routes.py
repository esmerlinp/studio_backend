from flask import Blueprint
from . import controller

student_charge_balances_bp = Blueprint('student_charge_balances', __name__, url_prefix='/api/v1/client/student-charge-balances')

student_charge_balances_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
