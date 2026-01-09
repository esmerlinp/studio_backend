from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import track_activity
from app.services.client_scheme.storage_service import remove_documents, get_documents, upload_document, get_document_by_id
from app.utils.responses import success, error



@jwt_required()
@track_activity
def get_document(document_id):
    user_id = get_jwt_identity()
    document=get_document_by_id(document_id=document_id, user_id=user_id)
    document_dic = document.to_dict()
    document_dic["url"] = document.temporary_url
    return success(data=document_dic)



@jwt_required()
@track_activity
def documents():
    user_id = get_jwt_identity()
    data = request.args
    entity_name = data.get("entity_name", None)
    
    documents = get_documents(user_id=user_id, entity_name=entity_name)
    return success(data=[d.to_dict() for d in documents])

@jwt_required()
@track_activity
def del_document(document_id):
    user_id = get_jwt_identity()
    remove_documents(user_id=user_id, document_id=document_id)
    return success(data={"remove": "ok"})

@jwt_required()
@track_activity
def add_document():
    user_id = get_jwt_identity() 
    data = request.args
    entity_name = data.get("entity_name", "general")
    entity_record = data.get("entity_record", None)
    file_name = data.get("file_name", None)
    
    if 'file' not in request.files:
        return error("No file provided", 400)
    
    file = request.files['file']


    try:

        file_storage = upload_document(user_id=user_id, file=file, entity_name=entity_name, entity_record=entity_record, file_name=file_name)

        return success(data=file_storage.to_dict(), message="Archivo subido con éxito")
    except Exception as e:
        return error(f"Fallo en el proceso: {str(e)}", 500)

