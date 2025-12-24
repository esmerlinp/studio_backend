from flask import request
from app.services import student_service
from flask_jwt_extended import jwt_required
from app import track_activity, require_role
from app.utils.responses import success, error
from app.utils import i18n

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