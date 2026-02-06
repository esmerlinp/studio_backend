from flask import Blueprint
from app.api.v1.master.dynamics import controller

# Definición del Blueprint con su prefijo de versión
dynamic_fields_bp = Blueprint('dynamic_fields', __name__, url_prefix='/api/v1/core/dynamics')

# --- RUTAS ---

# Obtener campos por entidad (Ej: /api/v1/dynamic-fields/STUDENT)
# Esta es la ruta que consultará tu Frontend para armar los formularios
dynamic_fields_bp.get("/<string:entityType>")(controller.get_entity_fields)

# Crear una nueva definición de campo
dynamic_fields_bp.post("/")(controller.create_field)

# (Opcional) Eliminar una definición de campo
# dynamic_fields_bp.delete("/<int:field_id>")(dynamic_field_controller.delete_field)