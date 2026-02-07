from flask import Blueprint
from . import controller

logs_webhooks_bp = Blueprint('logs_webhooks', __name__)

logs_webhooks_bp.add_url_rule('/logs-webhooks', view_func=controller.get_logs, methods=['GET'])
logs_webhooks_bp.add_url_rule('/logs-webhooks/<int:log_id>', view_func=controller.get_log, methods=['GET'])
logs_webhooks_bp.add_url_rule('/logs-webhooks', view_func=controller.create_log, methods=['POST'])
logs_webhooks_bp.add_url_rule('/logs-webhooks/<int:log_id>', view_func=controller.update_log, methods=['PUT'])
logs_webhooks_bp.add_url_rule('/logs-webhooks/<int:log_id>', view_func=controller.delete_log, methods=['DELETE'])
