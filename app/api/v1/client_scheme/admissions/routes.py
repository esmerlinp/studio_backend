from flask import Blueprint, request, jsonify, render_template, g
from . import controller
from app import limiter

admissions_bp = Blueprint('admissions', __name__)

# Internal routes (Protected by JWT and before_request)
@admissions_bp.route('/client/academic/admissions/create', methods=['GET'])
def internal_create():
    return controller.render_internal_form()

# Public routes (No JWT, identified by UUID)
@admissions_bp.route('/admissions/apply/<uuid>', methods=['GET'])
def public_apply_view(uuid):
    return controller.render_public_form(uuid)

@admissions_bp.route('/api/v1/public/admissions/catalogs/<uuid>', methods=['GET'])
@limiter.limit("10 per minute")
def public_catalogs(uuid):
    return controller.get_public_catalogs(uuid)

@admissions_bp.route('/api/v1/public/admissions/<uuid>', methods=['POST'])
@limiter.limit("5 per minute") # DDoS Protection as requested
def public_submit(uuid):
    return controller.submit_admission(uuid, is_public=True)

# Public document upload
@admissions_bp.route('/api/v1/public/admissions/<uuid>/documents', methods=['POST'])
@limiter.limit("10 per minute")
def public_upload_document(uuid):
    return controller.upload_public_admission_document(uuid)

# Internal API
@admissions_bp.route('/api/v1/client/admissions', methods=['POST'])
def internal_submit():
    return controller.submit_admission(is_public=False)

@admissions_bp.route('/api/v1/client/admissions/families', methods=['GET'])
def get_families():
    return controller.get_families()

@admissions_bp.route('/api/v1/client/admissions/families/<int:family_id>', methods=['GET'])
def get_family_detail(family_id):
    return controller.get_family_detail(family_id)

# Internal document upload
@admissions_bp.route('/api/v1/client/admissions/<int:admission_id>/documents', methods=['POST'])
def internal_upload_document(admission_id):
    return controller.upload_internal_admission_document(admission_id)
