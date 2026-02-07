from flask import Blueprint
from app.api.v1.master.clients.controller import (get_client_preferences, new_cliente, 
                                           get_logs, onboard_client,
                                           get_all_clients, get_client, get_plan, 
                                           change_plan, get_client_plans, 
                                           get_client_payments, handle_export_data,
                                           request_deletion, cancel_deletion, trigger_cleanup,
                                           update_client, toggle_client_status,
                                            get_client_users, get_client_storage, get_client_logs_admin,
                                            get_client_documents_list)


client_bp = Blueprint('clients', __name__, url_prefix='/api/v1/master/clients')

client_bp.get("/")(get_all_clients)
client_bp.get("/<int:clientId>")(get_client)
client_bp.get("/<int:clientId>/plan")(get_plan) #planes activos
client_bp.get("/<int:clientId>/plan/all")(get_client_plans) #todos los planes 
client_bp.get("/<int:clientId>/payments/orders")(get_client_payments)
client_bp.get("/settings")(get_client_preferences)
client_bp.get("/logs")(get_logs)

client_bp.patch("/plan/change")(change_plan)

client_bp.post("/")(new_cliente)
client_bp.post("/onboard")(onboard_client)
client_bp.post("/export-data")(handle_export_data)
client_bp.post("/request-deletion")(request_deletion)
client_bp.post("/cancel-deletion")(cancel_deletion)
client_bp.post("/cleanup")(trigger_cleanup)

client_bp.patch("/<int:clientId>")(update_client)
client_bp.patch("/<int:clientId>/status")(toggle_client_status)

# Client Details Endpoints
client_bp.get("/<int:clientId>/users")(get_client_users)
client_bp.get("/<int:clientId>/storage")(get_client_storage)
client_bp.get("/<int:clientId>/documents")(get_client_documents_list)
client_bp.get("/<int:clientId>/logs")(get_client_logs_admin)
