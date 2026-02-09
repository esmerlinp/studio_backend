from flask import render_template, request, jsonify, g
from app.models.master_scheme.client_model import Client
from app.models.client_scheme.admission_request_model import AdmissionRequest
from app.services.master_scheme.client_service import set_schema, get_client_by_uuid
from app.services.client_scheme.student_service import save_student_detail
from app.services.client_scheme.storage_service import upload_document
from app.services.master_scheme.user_client_service import get_client_by_user
from app import db, limiter
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.responses import success, error
import logging

# Catalog imports
from app.models.master_scheme.gender_model import Gender
from app.models.master_scheme.document_type_model import DocumentType
from app.models.master_scheme.profession_model import Profession
from app.models.master_scheme.marital_status_model import MaritalStatus
from app.models.master_scheme.medical_institution_model import MedicalInstitution
from app.models.master_scheme.health_insurance_institution_model import HealthInsuranceInstitution
from app.models.master_scheme.blood_type_model import BloodType
from app.models.master_scheme.other_school_model import OtherSchool
from app.models.master_scheme.phone_type_model import PhoneType
from app.models.master_scheme.allergy_model import Allergy
from app.models.master_scheme.country_model import Country
from app.models.master_scheme.city_model import City
from app.models.master_scheme.sector_model import Sector
from app.models.client_scheme.cycle_list_view import CycleListView
from app.models.client_scheme.course_list_view import CourseListView
from app.models.client_scheme.family_list_view import FamilyListView
from app.models.client_scheme.student_details_models import StudentFamily, StudentFamilyPhone, StudentFamilyEmail

def render_internal_form():
    """Renders the internal creation form."""
    return render_template('es/client/academic/admissions/create.html')

def render_public_form(uuid):
    """Renders the public admission form for a specific school."""
    client = get_client_by_uuid(uuid)
    if not client:
        return render_template('errors/404.html'), 404
    
    return render_template('es/client/academic/admissions/public_apply.html', 
                          client_name=client.name, 
                          client_uuid=uuid)

def get_public_catalogs(uuid):
    """Returns all necessary catalogs for the admission form publicly."""
    client = get_client_by_uuid(uuid)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    # Switch to client schema for courses/cycles
    set_schema(client.schemaName)
    
    catalogs = {
        'cycleId': [c.to_dict() for c in CycleListView.query.filter_by(isActive=True).all()],
        'courseId': [c.to_dict() for c in CourseListView.query.filter_by(isActive=True).all()],
        'genderId': [g.to_dict() for g in Gender.query.filter_by(is_active=True).all()],
        'f_docType': [d.to_dict() for d in DocumentType.query.filter_by(is_active=True).all()],
        'm_docType': [d.to_dict() for d in DocumentType.query.filter_by(is_active=True).all()],
        'f_prof': [p.to_dict() for p in Profession.query.all()],
        'm_prof': [p.to_dict() for p in Profession.query.all()],
        'f_marital': [m.to_dict() for m in MaritalStatus.query.filter_by(is_active=True).all()],
        'm_marital': [m.to_dict() for m in MaritalStatus.query.filter_by(is_active=True).all()],
        'med_inst': [i.to_dict() for i in MedicalInstitution.query.all()],
        'med_seg': [i.to_dict() for i in HealthInsuranceInstitution.query.all()],
        'med_blood': [b.to_dict() for b in BloodType.query.all()],
        'prev_school': [s.to_dict() for s in OtherSchool.query.filter_by(is_active=True).all()],
        'phoneTypes': [p.to_dict() for p in PhoneType.query.all()],
        'allergies': [a.to_dict() for a in Allergy.query.all()],
        'countries': [c.to_dict() for c in Country.query.filter_by(is_active=True).all()],
        'cities': [c.to_dict() for c in City.query.filter_by(is_active=True).all()],
        'sectors': [s.to_dict() for s in Sector.query.filter_by(is_active=True).all()]
    }
    
    return jsonify(catalogs), 200

@jwt_required()
def get_families():
    """Returns all families from the FamilyListView."""
    families = FamilyListView.query.all()
    return jsonify([f.to_dict() for f in families]), 200

@jwt_required()
def get_family_detail(family_id):
    """Returns full detail of a family including phones and emails."""
    family = StudentFamily.query.get(family_id)
    if not family:
        return jsonify({'message': 'Familia no encontrada'}), 404
    
    phones = StudentFamilyPhone.query.filter_by(familyId=family_id).all()
    emails = StudentFamilyEmail.query.filter_by(familyId=family_id).all()
    
    data = family.to_dict()
    data['phones'] = [p.to_dict() for p in phones]
    data['emails'] = [e.to_dict() for e in emails]
    
    return jsonify(data), 200

def submit_admission(uuid=None, is_public=False):
    """Handles the submission of an admission request."""
    data = request.get_json()
    
    if is_public:
        if not uuid:
            return jsonify({'message': 'Client UUID is required'}), 400
        client = get_client_by_uuid(uuid)
        if not client:
            return jsonify({'message': 'Client not found'}), 404
        set_schema(client.schemaName)
    
    try:
        # 1. Create the Admission Request (Solicitud)
        admission = AdmissionRequest(
            applicantName=f"{data.get('firstName', '')} {data.get('lastName', '')}",
            cycleId=data.get('cycleId'),
            courseId=data.get('courseId'),
            responsibleName=data.get('responsibleName'),
            responsiblePhone=data.get('responsiblePhone'),
            evaluationState=1, # PENDING
            requestProcessState='PENDIENTE'
        )
        db.session.add(admission)
        db.session.flush() # Get admission ID
        
        # 2. Save Student Details (reusing existing service)
        student_data = data.copy()
        student_data['requestId'] = admission.id
        
        # If familyId is provided from association, we might need to handle it.
        # save_student_detail handles studentFamilyId if present in data.
        
        student_id, error_msg = save_student_detail(None, student_data)
        
        if error_msg:
            db.session.rollback()
            return jsonify({'message': error_msg}), 400
            
        db.session.commit()
        return jsonify({
            'message': 'Solicitud enviada correctamente',
            'id': admission.id,
            'student_id': student_id
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in submit_admission: {str(e)}")
        return jsonify({'message': 'Error interno del servidor'}), 500

@limiter.limit("10 per minute")
def upload_public_admission_document(uuid):
    """
    Upload a document for a public admission request.
    Rate-limited to prevent abuse.
    """
    client = get_client_by_uuid(uuid)
    if not client:
        return error("Cliente no encontrado", status_code=404)
    
    set_schema(client.schemaName)
    
    if 'file' not in request.files:
        return error("No se ha proporcionado ningún archivo", status_code=400)
    
    file = request.files['file']
    admission_id = request.form.get('admission_id')
    
    if not admission_id:
        return error("Se requiere el ID de la solicitud", status_code=400)
    
    try:
        # Create a temporary user context for public uploads
        # We'll use a special user_id of 0 for public uploads
        from app.services.master_scheme.documents_service import upload_to_gcs, save_file_metadata
        from app.utils.helpers import get_file_size
        
        # Upload to GCS
        folder = f"tenant_{client.uuid}/ADMISSION_REQUEST_{admission_id}"
        file_size_mb = get_file_size(file)
        
        import uuid as uuid_lib
        import os
        from google.cloud import storage as gcs
        
        storage_client = gcs.Client()
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        bucket = storage_client.get_bucket(bucket_name)
        
        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{folder}/{uuid_lib.uuid4()}{extension}"
        
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(file, content_type=file.content_type)
        
        generation_id = blob.generation
        
        gcs_data = {
            "path": unique_filename,
            "version": generation_id
        }
        
        storage = save_file_metadata(
            cliente_id=client.clientId,
            entidad=f"ADMISSION_REQUEST_{admission_id}",
            record_id=admission_id,
            gcs_data=gcs_data,
            file_name=file.filename,
            content_type=file.content_type,
            file_size_mb=file_size_mb
        )
        
        return success(data=storage.to_dict(), message="Documento subido correctamente")
    except Exception as e:
        logging.error(f"Error uploading public admission document: {str(e)}")
        return error(f"Error al subir documento: {str(e)}", status_code=500)

@jwt_required()
def upload_internal_admission_document(admission_id):
    """
    Upload a document for an internal admission request.
    """
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return error("No se ha proporcionado ningún archivo", status_code=400)
    
    file = request.files['file']
    
    try:
        document = upload_document(
            user_id=user_id,
            file=file,
            entity_name=f"ADMISSION_REQUEST_{admission_id}",
            entity_record=admission_id
        )
        return success(data=document.to_dict(), message="Documento subido correctamente")
    except Exception as e:
        return error(f"Error al subir documento: {str(e)}", status_code=500)
