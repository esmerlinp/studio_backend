from app.services.client_scheme.role_service import get_all_roles, create_role, delete_role
from flask_jwt_extended import jwt_required
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils.types import Roles as r
from flask import request
from app.utils import i18n # Importar el módulo de idiomas

@jwt_required()
@track_activity
def get_roles():
    
    roles = get_all_roles()
    return success(data=[r.to_dict() for r in roles])

@jwt_required()
@track_activity
def remove_rol(role_id):
    
    response = delete_role(role_id)
    if response == 0:
        return error(message=i18n._("error.role.not_found_or_fail"), status_code=404)
    
    return success(data={"id": response}, message=i18n._("success.role.deleted"))    

@jwt_required()
@track_activity
@require_role([r.ADMIN, r.OWNER, r.ROOT])
def add_roles():
    data = request.json
    name = data.get("name")
    code = data.get("code")
    description = data.get("description")
    
    if code in (r.ROOT, r.OWNER, r.SUPER_ADMIN, r.SYS_ADMIN):
        return error(message=i18n._("error.role.reserved_code"), status_code=403)
    
    role = create_role(name=name, code=code, description=description)
    
    return success(data=role.to_dict())
    