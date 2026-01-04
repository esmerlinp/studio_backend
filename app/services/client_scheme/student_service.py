from typing import List, Optional, Dict, Any
from ...extensions import db
from app.models.client_scheme.student_model import Student # Ajusta el import según tu estructura
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.utils.helpers import generate_download_url, paginate_query
from flask import g


def get_all_students() -> dict:
    """Retorna todos los estudiantes del esquema actual."""
    
    query = Student.query\
        .order_by(Student.id)
    data_dict, data_model = paginate_query(query=query)
    return data_dict

def get_student_by_id(student_id: int) -> Optional[Student]:
    student = Student.query.get(student_id)
    if not student:
        return None

    # Generamos la URL firmada usando la ruta guardada en la DB
    if student.photoUrl:
        # Usamos setattr para crear un atributo que NO sea una columna de la DB
        # o simplemente lo asignamos a una propiedad nueva:
        student.temporary_url = generate_download_url(student.photoUrl)
    
    return student

def get_student_by_code(code: str) -> Optional[Student]:
    """Busca un estudiante por su código institucional."""
    return Student.query.filter_by(student_code=code).first()

def create_student(data: Dict[str, Any]) -> Student:
    """
    Crea un nuevo estudiante.
    'data' puede contener tanto campos fijos como el diccionario 'custom_attributes'.
    """
    


    # Función auxiliar para convertir strings a objetos date si es necesario
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            # Ajusta el formato '%Y-%m-%d' según cómo envíes la fecha desde el frontend
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None
    try:
        new_student = Student(
            requestId=data.get('requestId'),
            studentCode=data.get('studentCode'),
            # Convertimos strings a objetos date
            enrollmentDate=parse_date(data.get('enrollmentDate')) or datetime.utcnow().date(),
            birthDate=parse_date(data.get('birthDate')),
            
            # Nombres corregidos
            firstName=data.get('firstName'),
            middleName=data.get('middleName'),
            lastName=data.get('lastName'),
            secondLastName=data.get('secondLastName'),
            
            genderId=data.get('genderId'),
            livingSituation=data.get('livingSituation'),
            countryId=data.get('countryId'),
            cityId=data.get('cityId'),
            sectorId=data.get('sectorId'),
            address=data.get('address'),
            previousSchoolId=data.get('previousSchoolId'),
            entryReason=data.get('entryReason'),
            status=data.get('status', 1),
            familyId=data.get('familyId'),
            bloodTypeId=data.get('bloodTypeId'),
            
            # El campo dinámico que mantuvimos en snake_case
            custom_attributes=data.get('custom_attributes', {})
        )
        db.session.add(new_student)
        g.audit_new_values = new_student
                
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
        
        # 1. Guardar valores viejos (antes del cambio)
        g.audit_old_values = student.to_dict()
    
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

        
        # 3. Guardar valores nuevos (después del cambio)
        g.audit_new_values = data
    
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
        g.audit_old_values = student.to_dict()
        
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e