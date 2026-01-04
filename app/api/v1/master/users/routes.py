from flask import Blueprint
from app.api.v1.master.users.controller import get_user, get_users, create_user, me, get_user_by_name, change_password, forgot_password, add_default_user_preferences, update_user_preferences, get_my_client


users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

# GET
users_bp.get("/")(get_users)
users_bp.get("/<userId>")(get_user)
users_bp.get("/<string:userName>")(get_user_by_name)
users_bp.get("/current")(me)
users_bp.get("/current/client")(get_my_client)

# POSTS
users_bp.post("/")(create_user) 
users_bp.post("/changepassword")(change_password) 
users_bp.post("/forgot-password")(forgot_password) 


#PREFERENCES
# users_bp.post("/preferences")(add_user_preferences) 
users_bp.post("/preferences/default")(add_default_user_preferences) 
users_bp.put("/current/preferences")(update_user_preferences) 