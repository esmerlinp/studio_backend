from app.services.master_scheme import client_service
from app.models.master_scheme.client_storage_model import ClientStorage

def has_available_storage(client_id: int, new_file_size_mb: float) -> bool:
    """ Este servicio verificará si el cliente tiene espacio disponible antes de permitir una carga de archivo o la creación de un nuevo registro pesado (como una foto de estudiante)."""
    # 1. Obtener el plan del cliente y su límite
    client = client_service.get_client_by_id(client_id)
    plan_limit_gb = client.plan.storage_limit_gb
    plan_limit_mb = plan_limit_gb * 1024

    # 2. Obtener el uso actual
    storage_record = ClientStorage.query.filter_by(client_id=client_id).first()
    current_usage = storage_record.used_storage_mb if storage_record else 0

    # 3. Validar
    return (current_usage + new_file_size_mb) <= plan_limit_mb



