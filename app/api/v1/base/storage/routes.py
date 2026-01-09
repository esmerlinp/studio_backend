from flask import Blueprint
from app.api.v1.base.storage.controller import  documents, del_document, add_document, get_document

documents_bp = Blueprint('documents', __name__, url_prefix='/api/v1/documents')

documents_bp.get("/")(documents)
documents_bp.post("/upload")(add_document)
documents_bp.get("/<int:document_id>")(get_document)
documents_bp.delete("/<int:document_id>")(del_document)