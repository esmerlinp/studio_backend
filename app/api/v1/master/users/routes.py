from flask import Blueprint
from app.api.v1.master.notifications.controller import get_notifications
from app.api.v1.master.users.controller import (get_user, get_users, create_user, 
                                                me, get_user_by_name, change_password, 
                                                forgot_password, add_default_user_preferences, update_user_preferences, inactivate_user)

from app.api.v1.master.clients.controller import (get_my_institution, get_my_subscription,
                                                  get_my_payments, get_my_storage_usage, 
                                                  get_my_personal_logs, get_my_personal_logs_by_entity)

from app.api.v1.master.auth.controller import sessions
from app.api.v1.master.clients.controller import get_my_plan

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/user')

# GET
users_bp.get("/")(get_users)
users_bp.get("/<userId>")(get_user)
users_bp.put("/<userId>/desactivate")(inactivate_user) 
users_bp.get("/<userName>")(get_user_by_name)

users_bp.get("/me")(me)
users_bp.get("/organization")(get_my_institution)# Información de la institución (El "Client" de la tabla master.clientes)
users_bp.get("/subscription")(get_my_subscription)# Facturación y Suscripción
users_bp.get("/payments")(get_my_payments)
users_bp.get("/sessions")(sessions)

users_bp.get("/storage")(get_my_storage_usage)# Recursos y Seguridad
users_bp.get("/audit")(get_my_personal_logs)
users_bp.get("/audit/<string:entityName>")(get_my_personal_logs_by_entity)
users_bp.get("/notifications")(get_notifications)

users_bp.get("/plan")(get_my_plan) #planes activos


# POSTS
users_bp.post("/")(create_user) 
users_bp.post("/changepassword")(change_password) 
users_bp.post("/forgot-password")(forgot_password) 


#PREFERENCES
# users_bp.post("/preferences")(add_user_preferences) 
users_bp.post("/preferences/default")(add_default_user_preferences) 
users_bp.put("/preferences")(update_user_preferences) 
