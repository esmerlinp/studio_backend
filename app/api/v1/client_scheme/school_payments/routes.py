from flask import Blueprint
from . import controller

school_payments_bp = Blueprint('school_payments', __name__, url_prefix='/api/v1/client/school-payments')

school_payments_bp.add_url_rule('/', view_func=controller.get_all, methods=['GET'])
