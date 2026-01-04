import uuid
from google.cloud import storage
from flask import current_app
import os
from dotenv import load_dotenv
from app.utils.helpers import get_file_size
from app.services.master_scheme.user_client_service import get_client_by_user
from app.services.master_scheme import client_service

def upload_to_gcs(user_id, file,  location_folder="general"):
    """
    Sube un archivo a Google Cloud Storage.
    :param file: Objeto FileStorage de Flask
    :param foldlocation_folderer: Carpeta de destino dentro del bucket
    :return: URL del archivo subido
    """
    load_dotenv()
    try:
        
        cliente = get_client_by_user(user_id) # Identificar al colegio/cliente actual
        folder = f"tenant_{cliente.clientId}/{location_folder}"
        
        file_size_mb = get_file_size(file) # Función auxiliar para medir el archivo
        
        
        # B. Validar disponibilidad de espacio en el plan
        if not client_service.has_available_storage(cliente.clientId, file_size_mb):
            raise "Has alcanzado el límite de almacenamiento de tu plan. Mejora tu plan para subir más archivos."
        
       
        # 1. Configurar el cliente (Lee las credenciales de la var de entorno GOOGLE_APPLICATION_CREDENTIALS)
        client = storage.Client()
        bucket_name = os.getenv("GCS_BUCKET_NAME")
       
        bucket = client.get_bucket(bucket_name)

        # 2. Generar un nombre de archivo único
        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{folder}/{uuid.uuid4()}{extension}"

        # 3. Crear el blob (el objeto en GCS)
        blob = bucket.blob(unique_filename)

        # 4. Subir el archivo
        # content_type es importante para que el navegador lo abra correctamente
        blob.upload_from_file(file, content_type=file.content_type)

        # 5. Retornar la URL (Si el bucket es público)
        # Si es privado, deberías usar blob.generate_signed_url
        
        # Hacer el archivo público después de subirlo
        #blob.make_public()
        
         # IMPORTANTE: Actualizar el contador de uso
        client_service.update_client_storage_usage(cliente.clientId, file_size_mb)
        
        return unique_filename

    except Exception as e:
        print(f"Error en GCS Upload: {str(e)}")
        raise e