from flask import Blueprint
from app.api.v1.clients.controller import get_client_preferences, new_cliente, get_logs, onboard_client, get_storage_info


client_bp = Blueprint('clients', __name__, url_prefix='/api/v1/clients')

client_bp.get("/settings")(get_client_preferences)
client_bp.get("/logs")(get_logs)
client_bp.get("/storage-info")(get_storage_info)

client_bp.post("/")(new_cliente)
client_bp.post("/onboard")(onboard_client)


