import os
from google.cloud import storage
from datetime import datetime, timezone
from app import db
from app.models.client_scheme.storage_model import Storage
from app.services.master_scheme.user_client_service import get_client_by_user
from app.services.master_scheme.documents_service import upload_to_gcs, get_file_size
from app.services.master_scheme.client_service import update_client_storage_usage
from app.utils.helpers import generate_download_url
def get_documents(user_id, entity_name=None):
    """Obtiene todos los documentos activos de un cliente, opcionalmente filtrados por entidad."""
    cliente = get_client_by_user(user_id)
    query = Storage.query.filter_by(client_id=cliente.clientId, deleted_at=None)
    
    if entity_name:
        query = query.filter_by(entity=entity_name)
    
    return query.all()

def get_document_by_id(document_id, user_id):
    """Busca un documento específico por su ID primario."""
    
    cliente = get_client_by_user(user_id)
    doc = Storage.query.filter_by(id=document_id, deleted_at=None, client_id=cliente.clientId).first()
    if doc:
        doc.temporary_url = generate_download_url(doc.path_gcs)
        
    return doc


def upload_document(user_id, file, entity_name: str="general", entity_record=None, file_name=None) -> Storage:
    """
    Orquestador: Sube a GCS y registra metadatos en la DB.
    """
    
    # 2. Subir a Google Cloud Storage (Retorna path y version)
    nuevo_doc = upload_to_gcs(user_id, file, entity_name=entity_name, entity_record=entity_record, filename=file_name)

    return nuevo_doc

def remove_documents(user_id, document_id):
    """Realiza un borrado lógico en DB y elimina el objeto de GCS."""
    doc = Storage.query.get_or_404(document_id)
    
    
    # 1. Eliminar de Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket(os.getenv("GCS_BUCKET_NAME"))
    blob = bucket.blob(doc.path_gcs)
    blob.delete()
    
    
    # 2. Borrado lógico de la DB 
    doc.deleted_at = datetime.now(timezone.utc)
    db.session.commit()
    
        
    
    # IMPORTANTE: Actualizar el contador de uso
    cliente = get_client_by_user(user_id)
    update_client_storage_usage(cliente.clientId, float(doc.peso_mb), operation="subtract")
    
    
    return True