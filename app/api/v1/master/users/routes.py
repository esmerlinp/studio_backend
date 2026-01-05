from flask import Blueprint
from app.api.v1.master.notifications.controller import get_notifications
from app.api.v1.master.users.controller import (get_user, get_users, create_user, 
                                                me, get_user_by_name, change_password, 
                                                forgot_password, add_default_user_preferences, update_user_preferences, inactivate_user)

from app.api.v1.master.clients.controller import (get_my_institution, get_my_subscription,
                                                  get_my_payments, get_my_storage_usage, 
                                                  get_my_personal_logs, get_my_personal_logs_by_entity)

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

# GET
users_bp.get("/")(get_users)
users_bp.get("/<userId>")(get_user)
users_bp.put("/<userId>/desactivate")(inactivate_user) 
users_bp.get("/<userName>")(get_user_by_name)

users_bp.get("/current")(me)
users_bp.get("/current/organization")(get_my_institution)# Información de la institución (El "Client" de la tabla master.clientes)
users_bp.get("/current/subscription")(get_my_subscription)# Facturación y Suscripción
users_bp.get("/current/payments")(get_my_payments)

users_bp.get("/current/storage")(get_my_storage_usage)# Recursos y Seguridad
users_bp.get("/current/audit")(get_my_personal_logs)
users_bp.get("/current/audit/<string:entityName>")(get_my_personal_logs_by_entity)
users_bp.get("/current/notifications")(get_notifications)


# POSTS
users_bp.post("/")(create_user) 
users_bp.post("/changepassword")(change_password) 
users_bp.post("/forgot-password")(forgot_password) 


#PREFERENCES
# users_bp.post("/preferences")(add_user_preferences) 
users_bp.post("/preferences/default")(add_default_user_preferences) 
users_bp.put("/current/preferences")(update_user_preferences) 
