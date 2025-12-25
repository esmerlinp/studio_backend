from flask import request
from app.services import student_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils import i18n
from app.utils.helpers import get_file_size
from app.services.master_scheme import client_service
from app.services.master_scheme.user_client_service import get_client_by_user

@jwt_required()
@track_activity
def get_students():
    """Obtiene la lista de todos los estudiantes del esquema actual."""
    data = student_service.get_all_students()
    return success(data=[student.to_dict() for student in data])

@jwt_required()
@track_activity
def get_student(student_id: int):
    """Obtiene un estudiante específico por su ID."""
    student = student_service.get_student_by_id(student_id)
    if not student:
        return error(i18n.t("student.not_found"), 404)
    return success(data=student.to_dict())

@jwt_required()
@track_activity
def create_student():
    """Crea un nuevo estudiante incluyendo campos fijos y dinámicos."""
    data = request.get_json()
    
    if not data:
        return error(i18n.t("api.invalid_payload"), 400)

    try:
        new_student = student_service.create_student(data)
        return success(
            data=new_student.to_dict(), 
            msg=i18n.t("student.created_success"), 
            code=201
        )
    except Exception as e:
        return error(str(e), 400)

@jwt_required()
@track_activity
def update_student(student_id: int):
    """Actualiza datos de un estudiante (soporta actualización parcial)."""
    data = request.get_json()
    
    if not data:
        return error(i18n.t("api.invalid_payload"), 400)

    student = student_service.update_student(student_id, data)
    if not student:
        return error(i18n.t("student.not_found"), 404)

    return success(
        data=student.to_dict(), 
        msg=i18n.t("student.updated_success")
    )

@jwt_required()
@track_activity
@require_role(["ADMIN"])
def delete_student(student_id: int):
    """Elimina un estudiante del sistema."""
    deleted = student_service.delete_student(student_id)
    if not deleted:
        return error(i18n.t("student.not_found"), 404)
    
    return success(msg=i18n.t("student.deleted_success"))



@jwt_required()
def upload_student_file(student_id):
    user_id = get_jwt_identity() 
    
    if 'file' not in request.files:
        return error("No file provided", 400)
    
    file = request.files['file']
    
    cliente = get_client_by_user(user_id) # Identificar al colegio/cliente actual
    
    file_size_mb = get_file_size(file) # Función auxiliar para medir el archivo
    
    
    # B. Validar disponibilidad de espacio en el plan
    if not client_service.has_available_storage(cliente.clientId, file_size_mb):
        return error("Has alcanzado el límite de almacenamiento de tu plan. Mejora tu plan para subir más archivos.", 403)

    # Si hay espacio, proceder con la subida a Google Cloud Storage 
    try:
        from app.services.documents_service import upload_to_gcs
        #path = storage_service.upload(file)
        file_url = upload_to_gcs(file, folder=f"tenant_{cliente.clientId}/students")
       
        
        # IMPORTANTE: Actualizar el contador de uso
        client_service.update_client_storage_usage(cliente.clientId, file_size_mb)
        
        
        
        # E. (Opcional) Guardar URL en la DB del estudiante
        studen_data = {
            "photo_url": file_url
        }
        student_service.update_student(student_id=student_id, data=studen_data)

        
        return success(msg="Archivo subido con éxito")
    except Exception as e:
        return error(f"Fallo en el proceso: {str(e)}", 500)