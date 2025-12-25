from flask import request
from flask_jwt_extended import JWTManager
from app.api.v1.users.routes import users_bp
from app.api.v1.auth.routes import auth_bp
from app.api.v1.clients.routes import client_bp
from app.api.v1.plan.routes import plans_bp
from app.api.v1.student.routes import students_bp
from app.api.v1.dynamics.routes import dynamic_fields_bp
from app.api.v1.notifications.routes import notification_bp
from app.services.master_scheme.user_service import change_user_password, update_user, get_user_scheme, get_user_by_id
from app import create_app
from app.utils import i18n
from flask import render_template
from app.utils.helpers import verify_reset_token
from app.utils.responses import error
import os
from dotenv import load_dotenv
from app.extensions import db
from sqlalchemy import text

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

load_dotenv()

app = create_app()


jwt = JWTManager(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(students_bp)
app.register_blueprint(dynamic_fields_bp)
#TODO: Agregar el blueprint de Notificaciones cuando se cree la tabla

# ------------------------------
# Configuración de idioma
# ------------------------------
culture = "es-DO"
i18n.setup_gettext("es")


@app.route('/health')
def health():
    return 'OK', 200

# @app.route("/")
# def index():
#     users = User.query.all()
#     return {"users": [u.email for u in users]}


PUBLIC_ENDPOINTS = {
    "health",
    "main_page",
    "auth.login",
    "login",
    "plans_page",
    "plans.get_plans",
    "dashboard",
    "users.forgot_password",
    "confirmation_account",
    "reset_password",
    "reset_password_page",
    "clients.onboard_client"
}


@app.before_request
def set_schema():


    # 🔎 Endpoint actual
    endpoint = request.endpoint
    print(endpoint)
    # Si la ruta no existe (404), no intentes validar JWT
    if endpoint is None:
        return

    # 🔓 Endpoints públicos → NO validación de usuario
    if endpoint in PUBLIC_ENDPOINTS:
        db.session.execute(
            text("SET search_path TO public")
        )
        return

    # 🔐 A partir de aquí TODO requiere usuario
    verify_jwt_in_request()

    user_id = get_jwt_identity()
    if not user_id:
        return error("No autenticado", 401)

    user = get_user_by_id(user_id=user_id)
    if not user:
        return error("Usuario no existe", 401)

    if not user.isConfirmedUser:
        return error(
            "La cuenta no está confirmada. Revisa tu correo electrónico para activarla.",
            403
        )

    if user.mustChangePassword:
        return error(
            "Debes cambiar tu contraseña antes de continuar.",
            403
        )

    # 🔀 Cambiar schema del cliente
    schema_name = get_user_scheme(user_id=user_id)
    db.session.execute(
        text(f"SET search_path TO {schema_name}, public")
    )




@app.route("/")
def main_page():
    return render_template('es/main.html')


@app.route("/login")
def login():
    return render_template("es/login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("es/dashboard.html")



@app.route("/reset-password")
def reset_password_page():
    token = request.args.get("token")

    if not token or verify_reset_token(token) in (None, "expired"):
        return render_template("errors/token_invalid.html"), 400

    return render_template("emails/es/reset_password.html")


@app.route("/create-client")
def client_form():
    return render_template('es/create_client_page.html', 
                            submit_url='/login')
    
@app.route("/plans")
def plans_page():
    return render_template('es/plans.html', 
                            app_name=os.getenv("APP_NAME"))
    




@app.post("/auth/reset-password")
def reset_password():
    from app.extensions import db
    try:
        data = request.json 
        token = data.get("token")
        password = data.get("password")

        user_id = verify_reset_token(token, max_age=3600)

        if user_id in (None, "expired"):
            return {"error": "Token inválido o expirado"}, 400


        schema_name = get_user_scheme(user_id=user_id)
        db.session.execute(
            text(f"SET search_path TO {schema_name}, public")
        )
        
        user = change_user_password(user_id=user_id, new_password=password)
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        return {"message": "Contraseña actualizada correctamente"}
    except ValueError as e:
        return {
            "success": False,
            "errors": e.args[0]
        }, 400

    except LookupError:
        return {
            "success": False,
            "message": "Usuario no encontrado"
        }, 404
        
        
@app.route("/confirmation-account")
def confirmation_account():
    token = request.args.get("token")

    if not token or verify_reset_token(token) in (None, "expired"):
        return render_template("errors/token_invalid.html"), 400

    return render_template("es/confirmation_template.html")





if __name__ == '__main__':
        
    app.run(debug=True)
    # Usa la variable de entorno PORT si existe, de lo contrario 8080
    #port = int(os.environ.get("PORT", 8080))
    #app.run(host="0.0.0.0", port=port)
