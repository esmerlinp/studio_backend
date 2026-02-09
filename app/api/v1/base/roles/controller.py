from app.services.client_scheme.role_service import get_roles_by_client, create_role_for_client
from app.services.master_scheme.user_client_service import get_client_by_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils.types import Roles as r
from flask import request
from app.utils import i18n # Importar el módulo de idiomas

@jwt_required()
@track_activity
def get_roles():
    user_id = get_jwt_identity()
    client = get_client_by_user(user_id)
    if not client:
        return error(message="No client context found", status_code=400)
    
    roles = get_roles_by_client(str(client.uuid))
    return success(data=[r.to_dict() for r in roles])

@jwt_required()
@track_activity
def remove_rol(role_id):
    
    # Delete role functionality not yet implemented
    return error(message="Delete role not implemented yet", status_code=501)    

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
    
    role = create_role_for_client(
        client_uuid=str(client.uuid),
        data={"name": name, "code": code, "description": description}
    )
    
    return success(data=role.to_dict())
    