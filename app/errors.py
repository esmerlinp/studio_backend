import logging
import traceback
from flask import jsonify, request, g
from datetime import datetime

# Configuración básica del logging
logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

def register_error_handlers(app):
    
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Captura cualquier error no controlado (500)"""
        
        # 1. Extraemos el traceback completo para el log
        error_details = traceback.format_exc()
        
        # 2. Construimos el mensaje para nuestro archivo log
        log_msg = (
            f"\n--- ERROR INTERNO ---\n"
            f"Ruta: {request.url}\n"
            f"Método: {request.method}\n"
            f"Usuario: {getattr(g, 'user_id', 'Anónimo')}\n"
            f"Detalle: {error_details}"
        )
        
        # 3. Guardamos en el archivo akdmia_errors.log
        logging.error(log_msg)

        return jsonify({
            "status": "error",
            "msg": "Ha ocurrido un error inesperado.",
            "error_id": datetime.now().strftime("%Y%m%d%H%M%S") # Útil para que el cliente reporte
        }), 500
    
    
    
    @app.errorhandler(ValueError)
    def handle_bad_request(e):
        # 400: El cliente envió algo mal (un ID inexistente, un valor negativo, etc.)
        logging.warning(f"Validación fallida: {str(e)} en {request.url}")
        return jsonify({
            "status": "error",
            "error_type": "ValueError",
            "msg": str(e)
        }), 400

    @app.errorhandler(PermissionError)
    def handle_forbidden(e):
        # 403: El usuario está autenticado pero no tiene permiso para ese recurso
        logging.warning(f"El usuario está autenticado pero no tiene permiso para ese recurso: {str(e)} en {request.url}")
        return jsonify({
            "status": "error",
            "error_type": "PermissionError",
            "msg": str(e)
        }), 403

    @app.errorhandler(RuntimeError)
    def handle_conflict(e):
        # 409: Hay un conflicto con el estado actual (ej. NCF agotado)
        logging.warning(f"RuntimeError: {str(e)} en {request.url}")
        return jsonify({
            "status": "error",
            "error_type": "RuntimeError",
            "msg": str(e)
        }), 409

