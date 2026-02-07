from flask import request
from app import track_activity, require_role
from app.utils.responses import success, error
from app.services.master_scheme.ncf_service import NCFService
from app.utils.types import Roles as r
from flask_jwt_extended import jwt_required

ADMIN_ROLES = [r.OWNER, r.ADMIN, r.SUPER_ADMIN, r.SYS_ADMIN, r.ROOT]

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def get_sequences():
    sequences = NCFService.get_sequences()
    return success(data=[s.to_dict() for s in sequences])

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def create_sequence():
    data = request.get_json()
    try:
        type_ncf = data.get('type_ncf')
        prefix = data.get('prefix', 'B')
        start_num = data.get('start_num')
        max_num = data.get('max_num')
        expiration_date = data.get('expiration_date') # Formato string 'YYYY-MM-DD' recomendado
        
        # Validaciones básicas
        if not type_ncf or not start_num or not max_num:
            return error("Faltan datos obligatorios (tipo, inicio, máximo).", 400)
            
        new_seq = NCFService.create_sequence(
            type_ncf=type_ncf,
            prefix=prefix,
            start_num=int(start_num),
            max_num=int(max_num),
            expiration_date=expiration_date
        )
        return success(data=new_seq.to_dict(), message="Secuencia creada exitosamente")
    except Exception as e:
        return error(str(e), 500)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def toggle_sequence(sequence_id):
    active = request.args.get('active', 'true').lower() == 'true'
    if NCFService.toggle_sequence_status(sequence_id, active):
        return success(data={}, message="Estado de secuencia actualizado")
    return error("Secuencia no encontrada", 404)

@jwt_required()
@track_activity
@require_role(ADMIN_ROLES)
def get_logs():
    logs = NCFService.get_logs()
    return success(data=[l.to_dict() for l in logs])
