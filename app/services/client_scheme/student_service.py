from typing import List, Optional, Dict, Any
from ...extensions import db
from app.models.client_scheme.student_model import Student # Ajusta el import según tu estructura
from sqlalchemy.exc import SQLAlchemyError

def get_all_students() -> List[Student]:
    """Retorna todos los estudiantes del esquema actual."""
    return Student.query.all()

def get_student_by_id(student_id: int) -> Optional[Student]:
    """Busca un estudiante por su ID primario."""
    return Student.query.get(student_id)

def get_student_by_code(code: str) -> Optional[Student]:
    """Busca un estudiante por su código institucional."""
    return Student.query.filter_by(student_code=code).first()

def create_student(data: Dict[str, Any]) -> Student:
    """
    Crea un nuevo estudiante.
    'data' puede contener tanto campos fijos como el diccionario 'custom_attributes'.
    """
    try:
        new_student = Student(
            request_id=data.get('request_id'),
            student_code=data.get('student_code'),
            enrollment_date=data.get('enrollment_date'),
            last_name1=data.get('last_name1'),
            last_name2=data.get('last_name2'),
            first_name1=data.get('first_name1'),
            first_name2=data.get('first_name2'),
            gender_id=data.get('gender_id'),
            living_situation=data.get('living_situation'),
            birth_date=data.get('birth_date'),
            country_id=data.get('country_id'),
            city_id=data.get('city_id'),
            sector_id=data.get('sector_id'),
            address=data.get('address'),
            previous_school_id=data.get('previous_school_id'),
            entry_reason=data.get('entry_reason'),
            status=data.get('status', 1),
            family_id=data.get('family_id'),
            blood_type_id=data.get('blood_type_id'),
            # Los campos dinámicos se guardan aquí
            custom_attributes=data.get('custom_attributes', {})
        )
        
        db.session.add(new_student)
        db.session.commit()
        return new_student
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def update_student(student_id: int, data: Dict[str, Any]) -> Optional[Student]:
    """
    Actualiza un estudiante existente.
    Permite actualización parcial (patch) de campos fijos y dinámicos.
    """
    student = Student.query.get(student_id)
    if not student:
        return None

    try:
        # Actualización de campos fijos
        for key, value in data.items():
            if hasattr(student, key) and key != 'custom_attributes':
                setattr(student, key, value)
        
        # Actualización inteligente de campos dinámicos (Merge)
        if 'custom_attributes' in data:
            # Combinamos lo que ya existe con lo nuevo para no borrar datos previos
            current_attrs = dict(student.custom_attributes) if student.custom_attributes else {}
            current_attrs.update(data['custom_attributes'])
            student.custom_attributes = current_attrs

        db.session.commit()
        return student
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def delete_student(student_id: int) -> bool:
    """Elimina un estudiante por ID."""
    student = Student.query.get(student_id)
    if not student:
        return False
    
    try:
        db.session.delete(student)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e