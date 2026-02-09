from flask import Blueprint
from .controller import get_pos_data, checkout

cafeteria_api_bp = Blueprint('cafeteria_api', __name__)

cafeteria_api_bp.route('/pos-data', methods=['GET'])(get_pos_data)
cafeteria_api_bp.route('/checkout', methods=['POST'])(checkout)
