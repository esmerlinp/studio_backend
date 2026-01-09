from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.client_scheme.log_model import AuditLog
from ...extensions import db
from flask import g
from sqlalchemy import text

from datetime import datetime
from decimal import Decimal

def prepare_for_json(data):
    """Convierte recursivamente fechas y decimales en strings/floats para JSON."""
    if isinstance(data, dict):
        return {k: prepare_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [prepare_for_json(i) for i in data]
    elif isinstance(data, datetime):
        return data.isoformat() # Convierte fecha a "2026-01-09T..."
    elif isinstance(data, Decimal):
        return float(data)
    return data

@jwt_required(optional=True) # Permite entrar sin token
def log_action(
    action: str,
    resource_type: str,
    resource_id: int | None = None,
    description: str | None = None,
    old_values: dict | None = None,
    new_values: dict | None = None,
    user_id: int | None = None, # Parámetro manual
    status:str | None = None
):
    try:
        # 1. Intentar obtener identidad si user_id no fue pasado manualmente
        final_user_id = user_id
        if final_user_id is None:
            try:
                # get_jwt_identity() falla si se llama fuera de un contexto JWT protegido
                # sin el parámetro optional=True en decoradores, pero aquí lo manejamos:
                final_user_id = get_jwt_identity()
            except Exception:
                final_user_id = 0


        if not getattr(g, "scheme", None):
            # Intentamos el cambio directamente (es más rápido que preguntar si existe)
            return
        db.session.execute(text(f"SET search_path TO {g.scheme}"))
        
        # --- SOLUCIÓN AL ERROR DE SERIALIZACIÓN ---
        clean_old = prepare_for_json(old_values) if old_values else None
        clean_new = prepare_for_json(new_values) if new_values else None
        # --
                
        # 2. Crear el registro
        audit = AuditLog(
            user_id=final_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            # request.remote_addr puede fallar si no hay contexto de petición
            ip_address=request.remote_addr if request else "0.0.0.0",
            user_agent=request.headers.get("User-Agent") if request else "Internal/System",
            old_values=clean_old,
            new_values=clean_new,
            accion_type = status
            
        )
        
        db.session.add(audit)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error crítico en log_action: {str(e)}")