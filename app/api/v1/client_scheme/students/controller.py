from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.client_scheme.student_list_service import get_students
from app.services.client_scheme.student_service import get_full_student_detail
from app.services.client_scheme.storage_service import get_documents, upload_document, get_document_by_id, remove_documents
from app.utils.responses import success, error

@jwt_required()
def get_all():
    """
    Get all students.
    """
    filters = {}
    if request.args.get('cycleId'):
        filters['cycleId'] = request.args.get('cycleId', type=int)
        
    if request.args.get('levelId'):
        filters['levelId'] = request.args.get('levelId', type=int)
        
    if request.args.get('courseId'):
        filters['courseId'] = request.args.get('courseId', type=int)
        
    if request.args.get('studentStateId'):
        filters['studentStateId'] = request.args.get('studentStateId', type=int)
        
    data = get_students(filters)
        
    return jsonify([item.to_dict() for item in data]), 200

@jwt_required()
def get_by_id(id):
    """
    Get student by ID with full details.
    """
    data = get_full_student_detail(id)
    if not data:
        return jsonify({'message': 'Estudiante no encontrado'}), 404
        
    return jsonify(data), 200

@jwt_required()
def save(id=None):
    """
    Create or Update student details.
    """
    from app.services.client_scheme.student_service import save_student_detail
    data = request.get_json()
    
    student_id, error_msg = save_student_detail(id, data)
    
    if error_msg:
        return jsonify({'message': error_msg}), 400
        
    return jsonify({'message': 'Estudiante guardado correctamente', 'id': student_id}), 200

# Document Management Functions

@jwt_required()
def get_student_documents(student_id):
    """
    Get all documents for a specific student.
    """
    user_id = get_jwt_identity()
    try:
        documents = get_documents(user_id=user_id, entity_name=f"STUDENT_{student_id}")
        return success(data=[d.to_dict() for d in documents])
    except Exception as e:
        return error(f"Error al obtener documentos: {str(e)}", status_code=500)

@jwt_required()
def upload_student_document(student_id):
    """
    Upload a document for a specific student.
    """
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return error("No se ha proporcionado ningún archivo", status_code=400)
    
    file = request.files['file']
    
    try:
        document = upload_document(
            user_id=user_id,
            file=file,
            entity_name=f"STUDENT_{student_id}",
            entity_record=student_id
        )
        return success(data=document.to_dict(), message="Documento subido correctamente")
    except Exception as e:
        return error(f"Error al subir documento: {str(e)}", status_code=500)

@jwt_required()
def get_student_document(student_id, document_id):
    """
    Get a specific document with signed URL.
    """
    user_id = get_jwt_identity()
    try:
        document = get_document_by_id(document_id=document_id, user_id=user_id)
        if not document:
            return error("Documento no encontrado", status_code=404)
        
        document_dict = document.to_dict()
        document_dict["url"] = document.temporary_url
        return success(data=document_dict)
    except Exception as e:
        return error(f"Error al obtener documento: {str(e)}", status_code=500)

@jwt_required()
def delete_student_document(student_id, document_id):
    """
    Delete a specific document.
    """
    user_id = get_jwt_identity()
    try:
        remove_documents(user_id=user_id, document_id=document_id)
        return success(message="Documento eliminado correctamente")
    except Exception as e:
        return error(f"Error al eliminar documento: {str(e)}", status_code=500)
