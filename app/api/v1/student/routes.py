from flask import Blueprint
from app.api.v1.student import student_controller

students_bp = Blueprint('students', __name__, url_prefix='/api/v1/students')

students_bp.get("/")(student_controller.get_students)
students_bp.get("/<int:student_id>")(student_controller.get_student)
students_bp.post("/")(student_controller.create_student)
students_bp.patch("/<int:student_id>")(student_controller.update_student)
students_bp.delete("/<int:student_id>")(student_controller.delete_student)