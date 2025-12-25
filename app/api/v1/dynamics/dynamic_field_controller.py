from flask import request
from app.services import dynamic_field_service
from flask_jwt_extended import jwt_required
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils import i18n

@jwt_required()
@track_activity
def get_entity_fields(entity_type: str):
    """
    Endpoint para el Frontend:
    Retorna qué campos extras debe dibujar el formulario.
    """
    fields = dynamic_field_service.get_fields_by_entity(entity_type)
    return success(data=[f.to_dict() for f in fields])

@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN, ADMIN"])
def create_field():
    """Solo el Super Admin puede crear nuevas definiciones globales."""
    data = request.get_json()
    try:
        field = dynamic_field_service.create_dynamic_field(data)
        return success(data=field.to_dict(), msg="Campo definido correctamente", code=201)
    except Exception as e:
        return error(str(e), 400)