from typing import List, Dict, Any
from app import db
from app.models.client_scheme.dynamic_field_model import DynamicField # Importa tu clase DynamicField

def get_fields_by_entity(entity_type: str) -> List[DynamicField]:
    """Obtiene las definiciones de campos para una entidad (STUDENT, TEACHER, etc.)"""
    return DynamicField.query.filter_by(entityType=entity_type.upper()).all()

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
    db.session.add(new_field)
    db.session.commit()
    return new_field

def delete_dynamic_field(field_id: int) -> bool:
    field = DynamicField.query.get(field_id)
    if field:
        db.session.delete(field)
        db.session.commit()
        return True
    return False