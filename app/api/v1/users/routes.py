from flask import Blueprint
from app.api.v1.users.controller import get_user, get_users, create_user, me, get_user_by_name, change_password


users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

# GET
users_bp.get("/")(get_users)
users_bp.get("/<userId>")(get_user)
users_bp.get("/<string:userName>")(get_user_by_name)
users_bp.get("/me")(me)

# POSTS
users_bp.post("/")(create_user) 
users_bp.post("/changepassword")(change_password) 