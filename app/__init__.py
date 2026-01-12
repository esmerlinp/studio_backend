from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import mail, db, limiter
from app.services.master_scheme.session_service import get_session_active_by_user_id, invalidar_sesiones_por_id_session, actualizar_actividad_sesion
from app.services.master_scheme.log_service import log_action

from app.utils.responses import error
from app.models.master_scheme.user_model import User
from app.models.master_scheme.user_roles_model import UserRole
from app.models.master_scheme.roles_model import Role
from datetime import datetime, timezone
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import g, request
from app.errors import register_error_handlers


INACTIVITY_MINUTES = 30  # tiempo de inactividad permitido


# Funciona así:

# Lee el user_id del JWT.

# Busca la sesión activa en la base de datos.

# Si está expirada por inactividad → devuelve error 440.

# Si está activa → actualiza ultimo_acceso y renueva expiracion.



def create_app():
    load_dotenv()

    app = Flask(__name__)
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # cámbiala por una segura
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,  # Verifica si la conexión sirve antes de usarla
        "pool_recycle": 300,    # Recicla conexiones cada 5 minutos (evita que caduquen)
    }
    
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        FRONTEND_URL=os.getenv("BASE_URL"),

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
    
    # Vinculamos el limitador a la aplicación
    limiter.init_app(app)


    register_error_handlers(app)
    

    
    
    return app

def track_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()

            session = get_session_active_by_user_id(userId=user_id)

            if not session or not session.isActive:
                return jsonify({"msg": "Sesión inválida o expirada"}), 440
            
            # 2. VALIDACIÓN CRÍTICA: ¿El usuario sigue activo?
            # Esto detiene a los usuarios  que no pagaron
            user = User.query.get(user_id)
            
            if not user.isActive:                 
                return jsonify({
                    "msg": f"Cuenta inhabilitada. Contacte al administrador de su institución."
                }), 403


            expiration = session.expirationDate

            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            if expiration < now:
                invalidar_sesiones_por_id_session(sessionId=session.sessionId)
                return jsonify({"msg": "Sesión expirada por inactividad"}), 440

            # Actualizar actividad
            actualizar_actividad_sesion(sessionId=session.sessionId, inactivity_minutes=INACTIVITY_MINUTES)

            return func(*args, **kwargs)

        except Exception as e:
            print("track_activity error:", str(e))
            return error(message=f"Error en seguimiento de sesión {str(e)}", status_code=500)


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
            # --- PARTE 2: EJECUCIÓN DE LA FUNCIÓN ---
            response = fn(*args, **kwargs)

            # --- PARTE 3: AUDITORÍA (audit_log) ---
            # Solo auditamos si la respuesta fue exitosa (status 200-299)
            # Opcional: puedes quitar esta validación si quieres auditar intentos fallidos
            if isinstance(response, tuple):
                status_code = response[1]
            else:
                status_code = 200

            #if 200 <= status_code < 300:
            #resource_id = None
            resource_id = kwargs.get(resource_id_arg) if resource_id_arg in kwargs else None
            # Extraer valores guardados en 'g' durante la ejecución de la función
            old_vals = getattr(g, "audit_old_values", None)
            new_vals = getattr(g, "audit_new_values", None)
            audit_resource_id = getattr(g, "audit_resource_id", None)
            
            if audit_resource_id:
                resource_id = audit_resource_id
            
            user_id_from_jwt = get_jwt_identity()
            
            log_action(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                description=description,
                old_values=old_vals, # <--- Pasamos los diccionarios
                new_values=new_vals,
                user_id=user_id_from_jwt
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


