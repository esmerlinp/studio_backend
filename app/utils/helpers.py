from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from flask_mail import Message
from flask import render_template, current_app, request
from app.extensions import mail
import os
from dotenv import load_dotenv
from app.models.client_scheme.dynamic_field_model import DynamicField
from sqlalchemy import text
import datetime
from google.cloud import storage
from app import db
from app.utils import i18n

def schema_exists(schema_name):
    query = text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.schemata WHERE schema_name = :schema
        )
    """)
    result = db.session.execute(query, {"schema": schema_name}).scalar()
    return result

def paginate_query(query):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        "info": [item.to_dict() for item in pagination.items],
        "meta": {
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }
    }, pagination
    
def generate_download_url(blob_name):
    """Genera una URL firmada para un archivo específico."""
    storage_client = storage.Client()
    bucket_name = os.getenv("GCS_BUCKET_NAME")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # La URL expirará en 15 minutos
        expiration=datetime.timedelta(minutes=15),
        # Método permitido
        method="GET",
    )
    return url

def get_serializer():
    return URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt="password-reset"
    )


def generate_reset_token(user_id: int) -> str:
    serializer = get_serializer()
    return serializer.dumps({"user_id": user_id})


def verify_reset_token(token: str, max_age=1800):
    serializer = get_serializer()
    try:
        data = serializer.loads(
            token,
            max_age=max_age
        )
        return data["user_id"]
    except SignatureExpired:
        return "expired"
    except BadSignature:
        return None


def send_confirmation_account_email(user_id, user_name, email):
    load_dotenv()
    token = generate_reset_token(user_id)
    confirmation_url = f"{request.host_url}/confirmation-account?token={token}"
    
    send_email_template(subject=i18n._("email.subject.confirmation"),
                        to=[email],
                        path_template="emails/es/confirmation_email.html",
                        confirmation_url=confirmation_url, app_name=os.getenv("APP_NAME"), name=user_name
                        )
            
            
def send_reset_email(email: str, token: str, userName = ""):
    reset_url = f"{request.host_url}/reset-password?token={token}"

    msg = Message(
        subject=i18n._("email.subject.reset_password"),
        recipients=[email]
    )

    msg.html = render_template(
        "emails/es/reset_password_notify.html",
        reset_url=reset_url, name=userName, expiration_minutes="30"
    )

    mail.send(msg)
    
    
def send_email_template(subject:str, to:list[str], path_template, **kwargs):
 
    msg = Message(
        subject=subject,
        recipients=to
    )

    msg.html = render_template(
        path_template,
        **kwargs
    )

    mail.send(msg)
    
def send_email(subject:str, to:list[str], message):
 
    msg = Message(
        subject=subject,
        recipients=to,
        body=message
    )


    mail.send(msg)






def validate_custom_attributes(entity_type, attributes_dict):
    """
    Verifica que cada llave enviada en el JSON exista 
    en la tabla de definiciones para esa entidad.
    """
    # 1. Traer los nombres de campos permitidos desde 'master.dynamic_fields'
    allowed_fields = [
        f.name for f in DynamicField.query.filter_by(entity_type=entity_type).all()
    ]
    
    # 2. Comparar con lo que viene del frontend
    for key in attributes_dict.keys():
        if key not in allowed_fields:
            error_msg = i18n._("error.dynamic_field_undefined") % {
                'key': key, 
                'entity': entity_type
            }
            raise Exception(error_msg)

# En tu create_student llamarías a esta función:
# validate_custom_attributes('STUDENT', data.get('custom_attributes', {}))





def get_file_size(file_storage, unit="MB"):
    """
    Calcula el tamaño de un objeto FileStorage de Flask.
    
    :param file_storage: El objeto recuperado de request.files
    :param unit: 'B', 'KB', 'MB' o 'GB'
    :return: float con el tamaño en la unidad especificada
    """
    # 1. Mover el puntero al final del archivo para medir su longitud
    file_storage.seek(0, os.SEEK_END)
    size_in_bytes = file_storage.tell()
    
    # 2. IMPORTANTE: Regresar el puntero al inicio 
    # Si no haces esto, el archivo se subirá con 0 bytes a la nube
    file_storage.seek(0)
    
    # 3. Conversión de unidades
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3
    }
    
    size = size_in_bytes / units.get(unit.upper(), 1024**2)
    return round(size, 4)