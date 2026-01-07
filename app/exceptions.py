# exceptions.py o dentro de models.py
class AuditedError(Exception):
    """Excepción que dispara automáticamente un registro en la tabla de auditoría."""
    def __init__(self, message, resource_type, action_type, extra_data=None):
        super().__init__(message)
        self.message = message
        self.resource_type = resource_type  # Ej: ResourceTypes.NCF
        self.action_type = action_type      # Ej: ActionType.UPDATE
        self.extra_data = extra_data or {}   # Datos adicionales del error