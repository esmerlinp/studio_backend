from flask import request, redirect, render_template, jsonify
from flask_jwt_extended import JWTManager
from app.api.v1.master.users.routes import users_bp
from app.api.v1.master.auth.routes import auth_bp
from app.api.v1.master.clients.routes import client_bp
from app.api.v1.master.plan.routes import plans_bp
from app.api.v1.master.payments.routes import payment_bp, billing_bp
from app.api.v1.base.student.routes import students_bp
from app.api.v1.master.dynamics.routes import dynamic_fields_bp
from app.api.v1.master.notifications.routes import notification_bp
from app.api.v1.master.log.routes import admin_bp
from app.api.v1.master.country.routes import countries_bp
from app.services.master_scheme.user_service import change_user_password, update_user, get_user_scheme, get_user_by_id
from app import create_app
from app.utils import i18n
from app.utils.helpers import verify_reset_token, send_email
from app.utils.responses import error
import os
from dotenv import load_dotenv
from app.extensions import db
from sqlalchemy import text
from app.exceptions import AuditedError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from werkzeug.middleware.proxy_fix import ProxyFix



load_dotenv()

app = create_app()


app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1
)

jwt = JWTManager(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(plans_bp)
app.register_blueprint(students_bp)
app.register_blueprint(dynamic_fields_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(countries_bp)
app.register_blueprint(admin_bp)

# ------------------------------
# Configuración de idioma
# ------------------------------
culture = "es-DO"
i18n.setup_gettext("es")


#endpoints que consultas en esquema master que no requieren validacion de jwt
#aca no debe haber solicitudes a esquemas de clientes
MASTER_PUBLIC_ENDPOINTS = {
    "health",
    "host",
    "test_mail",
    "client_form",
    "main_page",
    "restore",
    "auth.login",
    "login",
    "plans_page",
    "plans.get_plans",
    "dashboard",
    "users.forgot_password",
    "confirmation_account",
    "reset_password",
    "reset_password_page",
    "clients.onboard_client",
    "payments.payment_success",
    "payments.stripe_webhook",
    "payments.cancel",
    "payments.show_restore_view",
    "countries.get_countries"
}


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "success": False,
        "msg": "Demasiadas peticiones. Por favor, intenta más tarde.",
        "description": str(e.description)
    }), 429


@app.route('/health')
def health():
    from app.utils.types import ResourceTypes, ActionType
    if 1==1:
        raise AuditedError(
                message="Intento de generar NCF con secuencia agotada",
                resource_type=ResourceTypes.NCF,
                action_type=ActionType.CREATE,
                extra_data={}
            )
    return 'OK', 200


@app.route("/host")
def host():
    return {"host": request.host_url}


@app.route('/test-mail')
def test_mail():
    try:
        import logging
        import smtplib

        # Esto forzará a imprimir el log del protocolo SMTP en la consola de Google Cloud
        smtplib.SMTP.debuglevel = 1 
        logging.basicConfig(level=logging.DEBUG)

        send_email(subject="Prueba Akdmia",
                      message="Si lees esto, el correo funciona desde Cloud Run",
                      to=["esmerlinep@gmail.com"])

        return "Correo enviado con éxito"
    except Exception as e:
        return f"Error enviando correo: {str(e)}"
    
    

def schema_exists(schema_name):
    query = text("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.schemata WHERE schema_name = :schema
        )
    """)
    result = db.session.execute(query, {"schema": schema_name}).scalar()
    return result

@app.before_request
def before_request():
    # 1. Forzar HTTPS
    if not request.is_secure and os.getenv('FLASK_ENV') != 'development':
        return redirect(request.url.replace('http://', 'https://', 1), code=301)
    
    endpoint = request.endpoint
    if endpoint is None:
        return

    print(endpoint)
    # 2. Excluir Webhooks y Públicos (VITAL para evitar errores de conexión en pagos)
    if request.path.startswith('/api/v1/payments/webhook') or endpoint in MASTER_PUBLIC_ENDPOINTS:
        # Aseguramos que los webhooks siempre operen sobre public
        #db.session.execute(text("SET search_path TO cliente"))
        return
    
    # 3. Validación de JWT
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except Exception:
        return error("No autenticado", 401)

    # 4. Obtener datos del usuario (Intenta optimizar esta función para que traiga el esquema de una vez)
    user = get_user_by_id(user_id=user_id)
    if not user:
        return error("Usuario no existe", 401)

    # ... tus validaciones de isConfirmedUser y mustChangePassword ...

    # 5. Cambio de Schema con Manejo de Errores Robusto
    schema_name = get_user_scheme(user_id=user_id)
    
    print(schema_name)
    
    # if not schema_name:
    #     return error("Ambiente no configurado", 500)

    try:
        # Intentamos el cambio directamente (es más rápido que preguntar si existe)
        db.session.execute(text(f"SET search_path TO {schema_name}, cliente"))
    except Exception as e:
        db.session.rollback()
        # Si falla, verificamos si es por conexión perdida o por esquema inexistente
        app.logger.error(f"Error al cambiar esquema a {schema_name}: {str(e)}")
        
        # Opcional: Aquí podrías llamar a schema_exists solo si falló el SET
        return error(
            "Su ambiente de trabajo no está disponible. Contacte a soporte.",
            500
        )
        
#@app.before_request
def set_schema_old():

    if not request.is_secure and os.getenv('FLASK_ENV') != 'development':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
    
    # 🔎 Endpoint actual
    endpoint = request.endpoint
    #print(endpoint)
    # Si la ruta no existe (404), no intentes validar JWT
    if endpoint is None:
        return

    if request.path.startswith('/api/v1/payments/webhook'):
        return
    
    # 🔓 Endpoints públicos → NO validación de usuario
    if endpoint in MASTER_PUBLIC_ENDPOINTS:
        # db.session.execute(
        #     text("SET search_path TO public")
        # )
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
    

    def schema_exists(schema_name):
        query = text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.schemata WHERE schema_name = :schema
            )
        """)
        result = db.session.execute(query, {"schema": schema_name}).scalar()
        return result
    
    try:
        if schema_name and schema_exists(schema_name):
            db.session.execute(
                text(f"SET search_path TO {schema_name}, public")
            )
        else:
             return error(
                "ha ocurrido un error al verificar su ambiente de trabajo, favor contacte a soporte de inmediato.",
                500
            )
    except Exception as e:
        db.session.rollback()
        # Intentar reconectar si la conexión se perdió
        db.session.execute(
            text(f"SET search_path TO {schema_name}, public")
        )


@app.route("/")
def main_page():
    return render_template('es/main.html')

@app.route("/billing/restore")
def restore():
    from app.models.master_scheme.client_model import Client
    import stripe
    load_dotenv()
    
    #user_id = user_id
    #relacion = UsuarioCliente.query.filter_by(user_id=user_id).first()
    #client_id = 68
    #data = request.get_json()
    client_id = request.args.get('clientId')
    client_id = request.args.get('clientId')
    
    if not client_id:
        return jsonify({"msg": "Falta el parámetro clientId"}), 400
    
    client = db.session.get(Client, client_id)
    
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    # Obtenemos el cliente de Stripe para ver su tarjeta predeterminada
    stripe_customer = stripe.Customer.retrieve(
        client.stripe_customer_id,
        expand=['invoice_settings.default_payment_method']
    )
    
    payment_method = stripe_customer.invoice_settings.default_payment_method
    
    if not payment_method:
        payment_methods = stripe.PaymentMethod.list(
            customer=client.stripe_customer_id,
            type="card",
            limit=1
        )
        if payment_methods.data:
            payment_method = payment_methods.data[0]
        
    
    card_data = {
        "last4": "****",
        "brand": "tarjeta",
        "exp_month": "--",
        "exp_year": "--"
    }
    
    if payment_method:
        card_data = {
            "last4": payment_method.card.last4,
            "brand": payment_method.card.brand,
            "exp_month": payment_method.card.exp_month,
            "exp_year": payment_method.card.exp_year
        }

    return render_template('es/restore_subscription.html', card=card_data, clientId=client.clientId)


@app.route("/login")
def login():
    app_name = os.getenv("APP_NAME")
    return render_template("es/login.html", app_name=app_name)

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
        print(schema_name)
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
        
    #app.run(debug=True)
    # Usa la variable de entorno PORT si existe, de lo contrario 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
