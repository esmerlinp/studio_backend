from flask import Blueprint
from .controller import get_roles, add_roles, remove_rol

roles_bp = Blueprint("roles", __name__, url_prefix="/api/v1/roles")

roles_bp.get("/")(get_roles)
roles_bp.post("/")(add_roles)
roles_bp.delete("/<int:role_id>")(remove_rol)

