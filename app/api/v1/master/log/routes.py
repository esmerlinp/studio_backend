
from flask import Blueprint, jsonify, request
from app.api.v1.master.log.controller import get_logs
# Asumiendo que usas algún decorador de roles
# from decorators import admin_required 

admin_bp = Blueprint('admin', __name__, url_prefix="/api/v1/master/admin")
admin_bp.get('/logs')(get_logs)
