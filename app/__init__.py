from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import mail, db
from app.services.master_scheme.session_service import get_session_active_by_user_id, invalidar_sesiones_por_id_session, actualizar_actividad_sesion
from app.services.master_scheme.log_service import log_action

from flask import abort
from sqlalchemy import text
from app.utils.responses import error
from app.models.master_scheme.user_model import User
from app.models.master_scheme.user_roles_model import UserRole
from app.models.master_scheme.roles_model import Role

INACTIVITY_MINUTES = 30  # tiempo de inactividad permitido


# Funciona así:

# Lee el user_id del JWT.

# Busca la sesión activa en la base de datos.

# Si está expirada por inactividad → devuelve error 440.

# Si está activa → actualiza ultimo_acceso y renueva expiracion.



def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # cámbiala por una segura
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        FRONTEND_URL=os.getenv("FRONTEND_URL"),

        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "true",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER"),
    )
    
    
    

    # 🔑 ESTA LÍNEA ES LA QUE TE FALTA
    mail.init_app(app)
    

    db.init_app(app)
  

    return app


def track_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            # Buscar la sesión activa del usuario
            # session = database.fetch_one("""
            #     SELECT * FROM usuariossesiones
            #     WHERE idusuario = %s AND bactivo = TRUE
            #     ORDER BY idusuariosesion DESC LIMIT 1
            # """, (user_id,))
            
            session = get_session_active_by_user_id(userId=user_id)

            if not session:
                return jsonify({"msg": "Sesión inválida"}), 440

            #now = datetime.now()
            from datetime import datetime, timezone
            # now = datetime.now(timezone.utc)
            # Si expiró por inactividad
            
            expiration = session.expirationDate

            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            if expiration < now:
                invalidar_sesiones_por_id_session(sessionId=session.sessionId)
                #database.execute_non_query("UPDATE usuariossesiones SET bactivo = FALSE WHERE idusuariosesion = %s", (session["idusuariosesion"],))
                return jsonify({"msg": "Sesión expirada por inactividad"}), 440

            # Actualizar actividad
            actualizar_actividad_sesion(sessionId=session.sessionId, inactivity_minutes=INACTIVITY_MINUTES)
            # database.execute_non_query("""
            #     UPDATE usuariossesiones 
            #     SET dultimoacceso = %s,
            #         dfechaexpiracion = %s
            #     WHERE idusuariosesion = %s
            # """, (
            #     now,
            #     now + timedelta(minutes=INACTIVITY_MINUTES),
            #     session["idusuariosesion"]
            # ))

            return func(*args, **kwargs)

        except Exception as e:
            print("track_activity error:", str(e))
            return jsonify({"msg": "Error en seguimiento de sesión"}), 500

    return wrapper

def audit_log(
    action: str,
    resource_type: str,
    resource_id_arg: str | None = None,
    description: str | None = None,
):
    """
    Decorador para registrar acciones en el audit log.

    Args:
        action: create | update | delete | read
        resource_type: nombre del recurso (employee, payroll, etc)
        resource_id_arg: nombre del argumento de la función que contiene el ID
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            response = fn(*args, **kwargs)

            resource_id = None
            if resource_id_arg and resource_id_arg in kwargs:
                resource_id = kwargs.get(resource_id_arg)

            log_action(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                description=description
            )

            return response

        return wrapper
    return decorator





def require_role(role_codes:list[str]):
    """
    Permite acceso si el usuario tiene AL MENOS UNO de los roles indicados.
    Ej:
        @require_role(["OWNER"])
        @require_role(["OWNER", "ADMIN"])
    """
    def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                user_id = get_jwt_identity()
                
                if not user_id:
                    return error("Usuario no autenticado", 401)
                
                # Validar que el usuario exista
                user = User.query.get(user_id)
                if not user:
                    return error("Usuario no existe", 403)

                # Obtener los roles válidos desde la tabla Role
                valid_roles = (
                    db.session.query(Role.id)
                    .filter(Role.code.in_(role_codes), Role.is_active == True)
                    .subquery()
                )

                # Verificar si el usuario tiene al menos uno de esos roles
                has_role = (
                    db.session.query(UserRole)
                    .filter(
                        UserRole.user_id == user_id,
                        UserRole.role_id.in_(valid_roles)
                    )
                    .first()
                )

                if not has_role:
                    return error(
                        f"Permisos insuficientes. Se requiere uno de: {', '.join(role_codes)}",
                        403
                    )

                return fn(*args, **kwargs)
            return wrapper
    return decorator


