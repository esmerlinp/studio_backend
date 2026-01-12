from typing import List, Dict, Any
from app import db
from flask import g
from app.models.client_scheme.dynamic_field_model import DynamicField # Importa tu clase DynamicField
from app import audit_log
from app.utils.types import ResourceTypes, ActionType

@audit_log(action=ActionType.READ, resource_type=ResourceTypes.DYNAMICS_FIELDS, resource_id_arg="entity_type")
def get_fields_by_entity(entity_type: str) -> List[DynamicField]:
    """Obtiene las definiciones de campos para una entidad (STUDENT, TEACHER, etc.)"""
    return DynamicField.query.filter_by(entityType=entity_type.upper()).all()

@audit_log(action=ActionType.CREATE, resource_type=ResourceTypes.DYNAMICS_FIELDS)
def create_dynamic_field(data: Dict[str, Any]) -> DynamicField:
    """Registra una nueva definición de campo en el esquema master."""
    
    new_field = DynamicField(
        entityType=data.get('entityType').upper(),
        label=data.get('label'),
        name=data.get('name'), # ej: 'talla_camisa'
        fieldType=data.get('fieldType'), # TEXT, SELECT, DATE
        isRequired=data.get('isRequired', False),
        options=data.get('options') # Lista de opciones si es SELECT
    )
    g.audit_new_values = new_field.to_dict()
    db.session.add(new_field)
    db.session.commit()
    return new_field

@audit_log(action=ActionType.DELETE, resource_type=ResourceTypes.DYNAMICS_FIELDS)
def delete_dynamic_field(field_id: int) -> bool:
    field = DynamicField.query.get(field_id)
    if field:
        g.audit_old_values = field.to_dict()
        db.session.delete(field)
        db.session.commit()
        return True
    return False