from flask import request
from app.services.client_scheme import dynamic_field_service
from flask_jwt_extended import jwt_required
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils import i18n
from app.utils.types import Roles as r


@jwt_required()
@track_activity
def get_entity_fields(entityType: str):
    """
    Endpoint para el Frontend:
    Retorna qué campos extras debe dibujar el formulario.
    """
    fields = dynamic_field_service.get_fields_by_entity(entityType)
    return success(data=[f.to_dict() for f in fields])

@jwt_required()
@track_activity
@require_role([r.ADMIN, r.OWNER, r.SUPER_ADMIN, r.SYS_ADMIN, r.ROOT])
def create_field():
    """Solo el Super Admin puede crear nuevas definiciones globales."""
    data = request.get_json()
    try:
        field = dynamic_field_service.create_dynamic_field(data)
        return success(data=field.to_dict(), msg=i18n._("success.dynamic_field.created"), code=201)
    except Exception as e:
        return error(str(e), 400)