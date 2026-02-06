from flask import Blueprint
from app.api.v1.base.student.controller import get_students, get_student, create_student, update_student, delete_student, upload_student_file

students_bp = Blueprint('students', __name__, url_prefix='/api/v1/core/students')

students_bp.get("/")(get_students)
students_bp.get("/<int:student_id>")(get_student)
students_bp.post("/")(create_student)
students_bp.patch("/<int:student_id>")(update_student)

students_bp.delete("/<int:student_id>")(delete_student)

students_bp.patch("/<int:student_id>/upload-image")(upload_student_file)