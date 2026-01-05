from flask import jsonify

def register_error_handlers(app):
    
    
    
    @app.errorhandler(ValueError)
    def handle_bad_request(e):
        # 400: El cliente envió algo mal (un ID inexistente, un valor negativo, etc.)
        return jsonify({
            "status": "error",
            "error_type": "ValueError",
            "msg": str(e)
        }), 400

    @app.errorhandler(PermissionError)
    def handle_forbidden(e):
        # 403: El usuario está autenticado pero no tiene permiso para ese recurso
        return jsonify({
            "status": "error",
            "error_type": "PermissionError",
            "msg": str(e)
        }), 403

    @app.errorhandler(RuntimeError)
    def handle_conflict(e):
        # 409: Hay un conflicto con el estado actual (ej. NCF agotado)
        return jsonify({
            "status": "error",
            "error_type": "RuntimeError",
            "msg": str(e)
        }), 409

    @app.errorhandler(Exception)
    def handle_internal_error(e):
        # 500: Errores no previstos (un fallo en la base de datos, bug en el código)
        # Aquí podrías integrar un log hacia Sentry o un archivo de logs
        print(f"DEBUG: Error no controlado: {str(e)}")
        return jsonify({
            "status": "error",
            "error_type": "InternalServerError",
            "msg": "Ha ocurrido un error inesperado en el servidor."
        }), 500