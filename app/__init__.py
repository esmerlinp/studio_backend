from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
from app.database import db


INACTIVITY_MINUTES = 30  # tiempo de inactividad permitido


# Funciona así:

# Lee el user_id del JWT.

# Busca la sesión activa en la base de datos.

# Si está expirada por inactividad → devuelve error 440.

# Si está activa → actualiza ultimo_acceso y renueva expiracion.


def track_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            # Buscar la sesión activa del usuario
            session = db.fetch_one("""
                SELECT * FROM usuariossesiones
                WHERE idusuario = %s AND bactivo = TRUE
                ORDER BY idusuariosesion DESC LIMIT 1
            """, (user_id,))

            if not session:
                return jsonify({"msg": "Sesión inválida"}), 440

            #now = datetime.now()
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            # Si expiró por inactividad
            if session["dfechaexpiracion"] < now:
                db.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion = %s", (session["idusuariosesion"],))
                return jsonify({"msg": "Sesión expirada por inactividad"}), 440

            # Actualizar actividad
            db.execute_non_query("""
                UPDATE usuariossesiones 
                SET dultimoacceso = %s,
                    dfechaexpiracion = %s
                WHERE idusuariosesion = %s
            """, (
                now,
                now + timedelta(minutes=INACTIVITY_MINUTES),
                session["idusuariosesion"]
            ))

            return func(*args, **kwargs)

        except Exception as e:
            print("track_activity error:", str(e))
            return jsonify({"msg": "Error en seguimiento de sesión"}), 500

    return wrapper