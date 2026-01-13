import uuid, os
from flask import g
from dotenv import load_dotenv
from app.utils.helpers import get_file_size
from app.services.master_scheme.user_client_service import get_client_by_user
from app.services.master_scheme import client_service
from app.exceptions import AuditedError
from app.utils.types import ResourceTypes, ActionType
from app.models.client_scheme.storage_model import Storage
from app import db
from app.utils import i18n, helpers  # Importar el módulo de idiomas
import os, uuid, subprocess
from datetime import timedelta
from google.cloud import storage
from app.models.master_scheme.client_model import Client




def save_file_metadata(cliente_id, entidad, record_id, gcs_data, file_name, content_type, file_size_mb):
    """
    Registra los metadatos de un archivo subido a Google Cloud Storage en la base de datos.

    Esta función crea un registro en la tabla 'cliente.almacenamiento' vinculando el 
    archivo físico en la nube con una entidad lógica del sistema (estudiantes, pagos, etc.).

    Args:
        cliente_id (int): ID único del cliente/colegio (tenant_id).
        entidad (str): Nombre de la categoría o tabla asociada (ej: 'ESTUDIANTE', 'PAGO').
        entidad_id (str|int): ID o UUID del registro específico al que pertenece el archivo.
        gcs_data (dict): Información técnica retornada por Google Cloud Storage.
            Debe contener:
            - 'path' (str): Ruta completa del objeto en el bucket.
            - 'version' (str|int): ID de generación/versión del objeto.
        file_info (dict): Información descriptiva del archivo original.
            Debe contener:
            - 'name' (str): Nombre original del archivo (ej: 'boletin.pdf').
            - 'type' (str): MIME type (ej: 'application/pdf').
            - 'size' (float): Tamaño del archivo en MB.

    Returns:
        Storage: El objeto de la clase Storage recién creado e insertado.

    Example:
        >>> gcs = {'path': 'tenant_1/docs/u4-123.pdf', 'version': '1715892'}
        >>> info = {'name': 'tarea.pdf', 'type': 'application/pdf', 'size': 2.5}
        >>> save_file_metadata(1, 'TAREA', 'TX-99', gcs, info)
    """
    nuevo_archivo = Storage(
        client_id=cliente_id,
        entity=entidad,
        record_id=str(record_id),
        file_name=file_name,
        path_gcs=gcs_data['path'],
        generation_id=str(gcs_data['version']),
        content_type=content_type,
        peso_mb=file_size_mb
    )
    db.session.add(nuevo_archivo)
    db.session.commit()
    return nuevo_archivo
    
    

def upload_to_gcs(user_id, file,  entity_name:str="general", entity_record:int = None, filename:str=None) -> Storage:
    """
    Sube un archivo a Google Cloud Storage.
    :param file: Objeto FileStorage de Flask
    :param foldlocation_folderer: Carpeta de destino dentro del bucket
    :return: URL del archivo subido
    """

    load_dotenv()
    try:
        
        cliente = get_client_by_user(user_id=user_id) # Identificar al colegio/cliente actual
       
        folder = f"tenant_{cliente.uuid}/{entity_name}"
        file_size_mb = get_file_size(file) # Función auxiliar para medir el archivo
        
        
        # B. Validar disponibilidad de espacio en el plan
        if not client_service.has_available_storage(cliente.clientId, file_size_mb):
            #raise "Has alcanzado el límite de almacenamiento de tu plan. Mejora tu plan para subir más archivos."
            error_msg = i18n._("error.storage.limit_reached")
            raise AuditedError(message=error_msg,
                               resource_type=ResourceTypes.STORAGE, action_type=ActionType.UPLOAD, user_id=user_id)
        
       
        # 1. Configurar el cliente (Lee las credenciales de la var de entorno GOOGLE_APPLICATION_CREDENTIALS)
        client = storage.Client()
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        bucket = client.get_bucket(bucket_name)

        
        unique_filename = ""
        
        # LÓGICA DE VERSIONAMIENTO:
        # Si envías un filename (ej: "logo_colegio.png"), usará ese.
        # Si no, genera uno único como hacías antes.
        if filename:
            unique_filename = f"{folder}/{filename}"
        else:
            # 2. Generar un nombre de archivo único
            extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{folder}/{uuid.uuid4()}{extension}"
        
        
        g.audit_new_values = unique_filename

        # 3. Crear el blob (el objeto en GCS)
        blob = bucket.blob(unique_filename)

        # 4. Subir el archivo
        # content_type es importante para que el navegador lo abra correctamente
        blob.upload_from_file(file, content_type=file.content_type)
        
        
        # El 'generation' es el ID específico de esta versión
        generation_id = blob.generation
        
        gcs_data = {
            "path": unique_filename,
            "version": generation_id
        }

        storage = save_file_metadata(cliente_id=cliente.clientId, entidad=entity_name, record_id=entity_record, gcs_data=gcs_data, file_name=file.filename, content_type=file.content_type, file_size_mb=file_size_mb)
        # 5. Retornar la URL (Si el bucket es público)
        # Si es privado, deberías usar blob.generate_signed_url
        
        # Hacer el archivo público después de subirlo
        #blob.make_public()
        
         # IMPORTANTE: Actualizar el contador de uso
        client_service.update_client_storage_usage(cliente.clientId, file_size_mb)
        
        

        
        return storage

    except Exception as e:
        print(f"Error en GCS Upload: {str(e)}")
        raise e
    




def export_client_data(app, schema_name, email):
    """
    Genera un archivo .sql del esquema del cliente y lo sube a GCS.
    """

    with app.app_context():
        load_dotenv()
        file_name = f"backup_{schema_name}_{uuid.uuid4().hex}.sql"
        local_path = f"/tmp/{file_name}"
        cliente = Client.query.filter_by(schemaName=schema_name).first()
        # Configuración de la base de datos (puedes sacarlo de tu config)
        db_uri = os.getenv("DATABASE_URL") 
        
        try:
            # 1. Ejecutar pg_dump solo para el esquema del cliente
            # El comando: pg_dump -n nombre_esquema > archivo.sql
            command = [
                "pg_dump",
                f"--schema={schema_name}",
                "--no-owner", # Para que el cliente pueda restaurarlo en otra DB
                f"--file={local_path}",
                db_uri
            ]
            
            subprocess.run(command, check=True)

            # 2. Subir a GCS en una carpeta de 'exports'
            client = storage.Client()
            bucket = client.bucket(os.getenv("GCS_BUCKET_NAME"))
            unique_filename = f"tenant_{cliente.uuid}/backup/{file_name}"
            blob = bucket.blob(unique_filename)
            
            blob.upload_from_filename(local_path)
            
            # 1. Refrescar los metadatos para asegurar que el atributo size esté disponible
            blob.reload()
            
            size_in_bytes = blob.size
            # 3. Convertir a MB (1 MB = 1024 * 1024 bytes)
            size_in_mb = size_in_bytes / (1024 * 1024)
            
            
            
            generation_id = blob.generation
        
            gcs_data = {
                "path": unique_filename,
                "version": generation_id
            }
            from sqlalchemy import text
            db.session.execute(text(f"SET search_path TO {schema_name}"))
            save_file_metadata(cliente_id=cliente.clientId, entidad="backup", record_id=0, gcs_data=gcs_data, file_name=blob.name, content_type=blob.content_type, file_size_mb=size_in_mb)

            # IMPORTANTE: Actualizar el contador de uso
            client_service.update_client_storage_usage(cliente.clientId, size_in_mb)
          

            # 3. Generar URL firmada válida por 1 hora
            url = blob.generate_signed_url(
                version="v4",
                # La URL expirará en 15 minutos
                expiration=timedelta(minutes=60),
                # Método permitido
                method="GET",
            )
            
            # Preparamos el contenido traducido
            helpers.send_email_template(
                subject=i18n._("email.subject.data_export_ready") % os.getenv("APP_NAME"),
                to=[email],
                path_template=f"emails/{i18n.get_locale()}/email_export.html",
                greeting=i18n._("email.export.greeting"),
                client_name=email,
                message_body=i18n._("email.export.message"),
                download_url=url,
                button_text=i18n._("email.export.button"),
                warning_text=i18n._("email.export.warning"),
                footer_text=i18n._("email.export.footer"),
                app_name=os.getenv("APP_NAME")
            )


            # Limpiar archivo local
            if os.path.exists(local_path):
                os.remove(local_path)

    

        except Exception as e:
            if os.path.exists(local_path):
                os.remove(local_path)
            raise Exception(i18n._("error.client.export_failed") % str(e))