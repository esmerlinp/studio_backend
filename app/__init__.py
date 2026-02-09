from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import mail, db, limiter, migrate
from app.services.master_scheme.session_service import get_session_active_by_user_id, invalidar_sesiones_por_id_session, actualizar_actividad_sesion
from app.services.master_scheme.log_service import log_action

from app.utils.responses import error
from app.models.master_scheme.user_model import User
from app.models.master_scheme.user_roles_model import UserRole
from app.models.master_scheme.roles_model import Role
from app.models.master_scheme.role_permission_model import RolePermission
from app.models.master_scheme.screen_functionality_model import ScreenFunctionality
from app.models.master_scheme.screen_model import Screen
from app.models.master_scheme.functionality_model import Functionality
from datetime import datetime, timezone
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import g, request, redirect
from sqlalchemy import select, text
from app.errors import register_error_handlers
from app.utils import i18n

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
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = os.getenv("FLASK_ENV") != "development"
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False # Simplified for now, consider enabling later
    
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
    migrate.init_app(app, db)
    
    # Vinculamos el limitador a la aplicación
    limiter.init_app(app)


    register_error_handlers(app)
    

    
    

    # Jinja Globals (Available in Macros)
    def url_args_without_page():
        args = request.args.copy()
        if 'page' in args:
            args.pop('page')
        return args
    
    app.jinja_env.globals['url_args_without_page'] = url_args_without_page

    # Initialize event bus subscribers
    with app.app_context():
        from app.services.client_scheme.communication_service import initialize_communication_subscribers
        initialize_communication_subscribers()

    return app

def track_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()

            session = get_session_active_by_user_id(userId=user_id)
            print("track_activity session:", session)
            if not session or not session.isActive:
                return jsonify({"msg": i18n._("auth.session_invalid")}), 440
            
            # 2. VALIDACIÓN CRÍTICA: ¿El usuario sigue activo?
            # Esto detiene a los usuarios  que no pagaron
            user = User.query.get(user_id)
            print("track_activity user:", user)
            if not user.isActive:                 
                return jsonify({
                    "msg": i18n._("auth.account_disabled")
                }), 403


            expiration = session.expirationDate
            print("track_activity expiration:", expiration)
            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)

            if expiration < now:
                invalidar_sesiones_por_id_session(sessionId=session.sessionId)
                return jsonify({"msg": i18n._("auth.session_expired_inactivity")}), 440
            # Actualizar actividad
            
            print("track_activity updating activity...")
            actualizar_actividad_sesion(sessionId=session.sessionId, inactivity_minutes=INACTIVITY_MINUTES)
            print("track_activity activity updated.")
            return func(*args, **kwargs)

        except Exception as e:
            print("track_activity error:", str(e))
            return error(message=f"{i18n._('auth.session_track_error')} {str(e)}", status_code=500)


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
                    return error(i18n._("auth.not_authenticated"), 401)
                
                # Validar que el usuario exista
                user = User.query.get(user_id)
                if not user:
                    return error(i18n._("auth.user_not_found"), 403)

                if role_codes is None or len(role_codes) == 0:
                    return fn(*args, **kwargs)
                
                try:
                    # Obtener los roles válidos desde la tabla Role
                    valid_roles_stmt = select(Role.id).where(Role.code.in_(role_codes), Role.is_active == True).scalar_subquery()
                    
                    # Verificar si el usuario tiene al menos uno de esos roles
                    has_role = (
                        db.session.query(UserRole)
                        .filter(
                            UserRole.user_id == user_id,
                            UserRole.role_id.in_(valid_roles_stmt)
                        )
                        .first()
                    )

                    if not has_role:
                        roles_str = ', '.join(role_codes)
                        msg = i18n._("auth.insufficient_permissions") % {'roles': roles_str}
                        if request.path.startswith('/api/'):
                            return error(msg, 403)
                        return redirect('/') # Or a specific forbidden page

                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error en require_role: {str(e)}")
                    return error(i18n._("system.error_processing_permissions"), 500)

                return fn(*args, **kwargs)
            return wrapper
    return decorator


def require_permission(screen_code: str, functionality_code: str):
    """
    Verifica si el usuario tiene permiso para acceder a una funcionalidad específica de una pantalla.
    Usa un enfoque sensible al contexto (Master vs Cliente).
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            
            if not user_id:
                return error(i18n._("auth.not_authenticated"), 401)
                
            # Verifica si el usuario es ROOT (acceso total a todo el sistema)
            is_root = (
                db.session.query(UserRole)
                .join(Role)
                .filter(UserRole.user_id == user_id, Role.code == "ROOT", Role.is_active == True)
                .first()
            )
            
            if is_root:
                return fn(*args, **kwargs)

            try:
                # 1. Determinar el contexto del cliente
                from app.services.master_scheme.user_client_service import get_client_by_user
                from app.services.master_scheme.permission_service import check_user_permission

                # Prioridad: Header -> Args -> Default del usuario
                client_uuid = request.headers.get('X-Client-UUID') or request.args.get('client_uuid')
                
                if not client_uuid:
                    client = get_client_by_user(user_id=user_id)
                    if client:
                        client_uuid = str(client.uuid)
                
                if not client_uuid:
                    app.logger.error(f"Permission check failed: No client context for user {user_id}")
                    return error(i18n._("auth.client_context_required"), 400)

                # 2. Verificar permiso usando el servicio unificado (fn_permisos_usuario)
                has_permission = check_user_permission(
                    user_id=int(user_id),
                    client_uuid=client_uuid,
                    screen_code=screen_code,
                    functionality_code=functionality_code
                )

                if not has_permission:
                    app.logger.warning(f"Access Denied: User {user_id} tried to access {screen_code}:{functionality_code} in client {client_uuid}")
                    if request.path.startswith('/api/'):
                        return error(i18n._("auth.insufficient_permissions"), 403)
                    return redirect('/')

                return fn(*args, **kwargs)

            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error checking permissions: {str(e)}")
                return error(i18n._("system.error_processing_permissions"), 500)

        return wrapper
    return decorator


