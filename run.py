from flask import request
from flask_jwt_extended import JWTManager
from app.api.v1.users.routes import users_bp
from app.api.v1.auth.routes import auth_bp
from app.api.v1.clients.routes import client_bp
from app.api.v1.plan.routes import plans_bp
from app.api.v1.notifications.routes import notification_bp
from app.services.user_service import change_user_password, update_user
from app import create_app
from app.utils import i18n
from flask import render_template
from app.utils.helpers import verify_reset_token

import os
from dotenv import load_dotenv

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

load_dotenv()

app = create_app()


jwt = JWTManager(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(plans_bp)
#TODO: Agregar el blueprint de Notificaciones cuando se cree la tabla

# ------------------------------
# Configuración de idioma
# ------------------------------
culture = "es-DO"
i18n.setup_gettext("es")


# @app.route('/')
# def hola_mundo():
#     return '¡Hola desde Flask!'

# @app.route("/")
# def index():
#     users = User.query.all()
#     return {"users": [u.email for u in users]}




@app.before_request
def set_schema():
    from app.extensions import db
    from sqlalchemy import text
    
    # Intenta validar JWT si existe (NO obligatorio)
    verify_jwt_in_request(optional=True)
    
    user_id = get_jwt_identity()

    if not user_id:
        return
    #TODO: Tomar el scheme de la tabla de clientes y pasarlo a la variable
    #User.query.filter_by(userId = user_id)
    #User.schema_name
 
    schema_name = "cliente"
    db.session.execute(
        text(f"SET search_path TO {schema_name}, public")
    )




# @app.route('/')
# def home():
#     host = request.host  # Ej: "localhost:5000"
#     url_completa = request.host_url  # Ej: "http://localhost:5000/"
#     return f"URL del servidor: {url_completa} - {host}"



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
def plans():
    return render_template('es/plans.html', 
                            app_name=os.getenv("APP_NAME"))
    
@app.route("/")
def main_page():
    return render_template('es/main.html')



@app.post("/auth/reset-password")
def reset_password():
    try:
        data = request.json 
        token = data.get("token")
        password = data.get("password")

        user_id = verify_reset_token(token)

        if user_id in (None, "expired"):
            return {"error": "Token inválido o expirado"}, 400

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
    try:
        token = request.args.get("token")
        user_id = verify_reset_token(token, max_age=24*60*60) #24 horas de expiracion
        if not token or user_id in (None, "expired"):
            return render_template('es/token_invalid.html', 
                                        status='error', 
                                        app_name=os.getenv("APP_NAME"), 
                                        resend_url='/resend-email')

    
        update_user(user_id=user_id, is_confirmed_user=True)
        return render_template('es/landing_page.html', 
                                status='success', 
                                app_name=os.getenv("APP_NAME"), 
                                login_url='/login')
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





if __name__ == '__main__':
        
    app.run(debug=True)
