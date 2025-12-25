from flask import request
from app.services.client_scheme import student_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils import i18n
from app.services.master_scheme.documents_service import upload_to_gcs

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
        return error(i18n._("student.not_found"), 404)
    return success(data=student.to_dict())

@jwt_required()
@track_activity
def create_student():
    """Crea un nuevo estudiante incluyendo campos fijos y dinámicos."""
    data = request.get_json()
    
    if not data:
        return error(i18n._("api.invalid_payload"), 400)

    try:
        new_student = student_service.create_student(data)
        return success(
            data=new_student.to_dict(), 
            message=i18n.t("student.created_success"), 
            code=201
        )
    except Exception as e:
        return error(str(e), 400)

@jwt_required()
@track_activity
def update_student(student_id: int):
    """Actualiza datos de un estudiante (soporta actualización parcial)."""
    data = request.get_json()
    print("student_id ", student_id)
    if not data:
        return error(i18n._("api.invalid_payload"), 400)

    student = student_service.update_student(student_id, data)
    if not student:
        return error(i18n._("student.not_found"), 404)

    return success(
        data=student.to_dict(), 
        message=i18n._("student.updated_success")
    )

@jwt_required()
@track_activity
@require_role(["ADMIN"])
def delete_student(student_id: int):
    """Elimina un estudiante del sistema."""
    deleted = student_service.delete_student(student_id)
    if not deleted:
        return error(i18n._("student.not_found"), 404)
    
    return success(message=i18n._("student.deleted_success"))



@jwt_required()
@track_activity
def upload_student_file(student_id):
    user_id = get_jwt_identity() 
    
    if 'file' not in request.files:
        return error("No file provided", 400)
    
    file = request.files['file']

    try:
        
        file_url = upload_to_gcs(user_id, file, location_folder="students")

        studen_data = {
            "photoUrl": file_url
        }
        data = student_service.update_student(student_id=student_id, data=studen_data)

        
        return success(data=data.to_dict(), message="Archivo subido con éxito")
    except Exception as e:
        return error(f"Fallo en el proceso: {str(e)}", 500)