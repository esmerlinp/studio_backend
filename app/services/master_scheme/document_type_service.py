from app.extensions import db
from app.models.master_scheme.document_type_model import DocumentType

def get_document_types():
    return DocumentType.query.all()

def get_document_type_by_id(dt_id):
    return DocumentType.query.get(dt_id)

def create_document_type(data):
    dt = DocumentType(**data)
    db.session.add(dt)
    db.session.commit()
    return dt

def update_document_type(dt_id, data):
    dt = DocumentType.query.get(dt_id)
    if dt:
        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
    return dt

def delete_document_type(dt_id):
    dt = DocumentType.query.get(dt_id)
    if dt:
        db.session.delete(dt)
        db.session.commit()
        return True
    return False
