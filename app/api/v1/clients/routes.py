from flask import Blueprint
from app.api.v1.clients.controller import get_client_preferences


client_bp = Blueprint('clients', __name__, url_prefix='/api/v1/clients')

client_bp.get("/settings")(get_client_preferences)