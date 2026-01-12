import logging
import traceback
from flask import request, g
from datetime import datetime
from app.exceptions import AuditedError
from app import log_action
from app.utils.responses import error
from app.utils.types import ActionType

# Configuración básica del logging
logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

def register_error_handlers(app):
    

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return error(message={
                "msg": "Demasiadas peticiones. Por favor, intenta más tarde.",
                "description": str(e.description)
                }, status_code=429)  
    
    @app.errorhandler(AuditedError)
    def handle_audited_error(e):

        # 1. Registrar en la tabla de auditoría (DB)
        # Usamos los datos que vienen dentro de la excepción
        if getattr(g, "scheme", None):
            log_action(
                action=e.action_type,
                resource_type=e.resource_type,
                description=f"OPERACIÓN FALLIDA: {e}",
                new_values=e.extra_data,
                user_id=e.user_id,
                status="ERROR" # Puedes agregar un campo status a tu tabla de auditoría
            )
        else:
            # 2. También lo guardamos en el archivo .log para el equipo técnico
           
            logging.warning(f"AuditedError: {e} | User: {g.get('user_id')}")

        # 3. Respondemos al Frontend
        return error(message={
            "status": "error",
            "msg": e.message,
            "type": e.action_type
        }, status_code=e.status_code)
    
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Captura cualquier error no controlado (500)"""
        # 1. Extraemos el traceback completo para el log
        error_details = traceback.format_exc()
        
        if getattr(g, "scheme", None):
            log_action(
                action=ActionType.ERROR,
                resource_type=request.method,
                description=f"OPERACIÓN FALLIDA: {e}\n Usuario: {getattr(g, 'user_id', 'Anónimo')}",
                new_values={error_details},
                status="FAILED" # Puedes agregar un campo status a tu tabla de auditoría
            )
        else:
            log_msg = (
                f"\n--- ERROR INTERNO ---\n"
                f"Ruta: {request.url}\n"
                f"Método: {request.method}\n"
                f"Usuario: {getattr(g, 'user_id', 'Anónimo')}\n"
                f"Detalle: {error_details}"
            )
                    
            logging.error(log_msg)

        return error(
            message={
            "status": "error",
            "msg": "Ha ocurrido un error inesperado.",
            "error_id": datetime.now().strftime("%Y%m%d%H%M%S")}, 
            status_code=500)
    
    
    
    @app.errorhandler(ValueError)
    def handle_bad_request(e):
        # 400: El cliente envió algo mal (un ID inexistente, un valor negativo, etc.)

        error_details = traceback.format_exc()
        if getattr(g, "scheme", None):
            log_action(
                action=ActionType.ERROR,
                resource_type=request.method,
                description=f"OPERACIÓN FALLIDA: {e}\n Usuario: {getattr(g, 'user_id', 'Anónimo')}",
                new_values={error_details},
                status="FAILED" # Puedes agregar un campo status a tu tabla de auditoría
            )
        else:
            logging.warning(f"Validación fallida: {str(e)} en {request.url}")


        return error(message={
            "status": "error",
            "error_type": "ValueError",
            "msg": str(e)
        })

    @app.errorhandler(PermissionError)
    def handle_forbidden(e):
        # 403: El usuario está autenticado pero no tiene permiso para ese recurso

            
        error_details = traceback.format_exc()
        if getattr(g, "scheme", None):
            log_action(
                action=ActionType.ERROR,
                resource_type=request.method,
                description=f"El usuario está autenticado pero no tiene permiso para ese recurso: {str(e)} en {request.url}\n Usuario: {getattr(g, 'user_id', 'Anónimo')}",
                new_values={error_details},
                status="FAILED" # Puedes agregar un campo status a tu tabla de auditoría
            )
        else:
            logging.warning(f"El usuario está autenticado pero no tiene permiso para ese recurso: {str(e)} en {request.url}")
            
        return error(message={
            "status": "error",
            "error_type": "PermissionError",
            "msg": str(e)
        }, status_code=403)

    @app.errorhandler(RuntimeError)
    def handle_conflict(e):

        # 409: Hay un conflicto con el estado actual (ej. NCF agotado)
        error_details = traceback.format_exc()

        if getattr(g, "scheme", None):
            log_action(
                action=ActionType.ERROR,
                resource_type=request.method,
                description=f"RuntimeError: {str(e)} en {request.url} en {request.url}\n Usuario: {getattr(g, 'user_id', 'Anónimo')}",
                new_values={error_details},
                status="FAILED" # Puedes agregar un campo status a tu tabla de auditoría
            )
        else:
            logging.warning(f"RuntimeError: {str(e)} en {request.url}")
           
            
        return error(message={
            "status": "error",
            "error_type": "RuntimeError",
            "msg": str(e)
        }, status_code=409)

