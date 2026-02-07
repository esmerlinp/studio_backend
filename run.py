from flask import request, redirect, render_template, jsonify, g
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
from app.api.v1.base.storage.routes import documents_bp
from app.api.v1.master.intelligence.routes import intelligence_bp
from app.api.v1.master.ncf.routes import ncf_bp
from app.api.v1.base.roles.routes import roles_bp
from app.services.master_scheme.user_service import change_user_password, get_user_scheme, get_user_by_id
from app import create_app, require_role
from app.utils import i18n
from app.utils.helpers import verify_reset_token
from app.utils.responses import error
import os
from dotenv import load_dotenv
from app.extensions import db
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, JWTManager, get_jwt, jwt_required
from werkzeug.middleware.proxy_fix import ProxyFix

import pytz

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
app.register_blueprint(documents_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(intelligence_bp)
app.register_blueprint(ncf_bp, url_prefix='/api/v1/master/ncf')

# ------------------------------
# Configuración de idioma
# ------------------------------
#culture = "es-DO"
#i18n.setup_gettext("en")


#endpoints que consultas en esquema master que no requieren validacion de jwt
#aca no debe haber solicitudes a esquemas de clientes
MASTER_PUBLIC_ENDPOINTS = {
    "health",
    "client_form",
    "main_page",
    "restore",
    "auth.login",
    "login",
    "plans_page",
    "plans.get_plans",
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



@app.route('/health')
def health():
    from flask_limiter.util import get_remote_address
    get_remote_address()
    return f'OK - {get_remote_address()}', 200
           


@app.route("/logout")
def logout_dashboard():
    from flask_jwt_extended import unset_jwt_cookies
    response = redirect("/login")
    unset_jwt_cookies(response)
    # Opcional: Inhabilitar sesión en DB si se desea mayor seguridad
    # Pero para un logout simple de UI, esto es suficiente si el token vive en cookies
    return response

@app.before_request
def load_user_preferences():
    # Simulamos obtener las preferencias del usuario (pueden venir de session o JWT)
    # En un caso real: prefs = get_jwt_identity().get('preferences')
    
    verify_jwt_in_request(optional=True)
    claims = get_jwt()
    
    # 2. Si el token existe y tiene el claim 'lang'
    if claims: 

        # Guardamos en 'g' para acceso global en este request
        g.date_format = claims.get('dateFormat').replace('DD', '%d').replace('MM', '%m').replace('YYYY', '%Y')
        g.hour_format = "%H:%M" if claims.get('hourFormat') == "24" else "%I:%M %p"
        g.tz = pytz.timezone(claims.get('timeZone', 'UTC'))
        g.lang = claims.get('language', 'es')
        
        i18n.setup_gettext(g.lang)
    else:
        # Valores por defecto
        g.date_format = "%d-%m-%Y"
        g.hour_format = "%H:%M"
        g.tz = pytz.timezone('UTC')
        g.lang = 'es'
        i18n.setup_gettext(g.lang)
        
    
@app.before_request
def before_request():
    # 1. Forzar HTTPS
    if not request.is_secure and os.getenv('FLASK_ENV') != 'development':
        return redirect(request.url.replace('http://', 'https://', 1), code=301)
    
    load_user_preferences()
    
    endpoint = request.endpoint
    if endpoint is None:
        return

    print(endpoint)
    # 2. Excluir Webhooks y Públicos (VITAL para evitar errores de conexión en pagos)
    if request.path.startswith('/api/v1/master/payments/webhook') or endpoint in MASTER_PUBLIC_ENDPOINTS:
        # Aseguramos que los webhooks siempre operen sobre public
        #db.session.execute(text("SET search_path TO cliente"))
        return
    
    # 3. Validación de JWT
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        g.user_id = user_id
        
    except Exception:
        if request.path.startswith('/api/'):
            return error(i18n._("auth.not_authenticated"), 401)
        return redirect('/login')

    # 4. Obtener datos del usuario (Intenta optimizar esta función para que traiga el esquema de una vez)
    user = get_user_by_id(user_id=user_id)
    if not user:
        return error(i18n._("auth.user_not_found"), 401)

    # ... tus validaciones de isConfirmedUser y mustChangePassword ...

    # 5. Cambio de Schema con Manejo de Errores Robusto
    schema_name = get_user_scheme(user_id=user_id)
 
    try:
        # Intentamos el cambio directamente (es más rápido que preguntar si existe)
        db.session.execute(text(f"SET search_path TO {schema_name}"))
        g.scheme = schema_name
        
    except Exception as e:
        db.session.rollback()
        # Si falla, verificamos si es por conexión perdida o por esquema inexistente
        app.logger.error(f"Error al cambiar esquema a {schema_name}: {str(e)}")
        
        # Opcional: Aquí podrías llamar a schema_exists solo si falló el SET
        return error(i18n._("system.environment_unavailable"), 500)

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
        return jsonify({"msg": i18n._("common.missing_client_id")}), 400
    
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
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard():
    from app.services.master_scheme.dashboard_service import get_admin_dashboard_data
    data = get_admin_dashboard_data()
    return render_template("es/dashboard.html", 
                         stats=data.get('stats'), 
                         recent_clients=data.get('recent_clients'), 
                         recent_payments=data.get('recent_payments'))

@app.route("/dashboard/clients")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_clients():
    from app.services.master_scheme.client_service import get_clients
    clients = get_clients()
    return render_template("es/dashboard/clients.html", clients=[c.to_dict() for c in clients])

@app.route("/dashboard/clients/<int:clientId>")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_client_details(clientId):
    # We pass the ID and let the frontend fetch the details via API
    return render_template("es/dashboard/client_details.html", clientId=clientId)

@app.route("/dashboard/clients/create")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_create_client():
    return render_template("es/dashboard/create_client.html")

@app.route("/dashboard/plans")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_plans():
    from app.models.master_scheme.plans_model import Plan
    from app.models.master_scheme.price_list_model import PriceList  # Required for relationship mapping
    
    plans = Plan.query.order_by(Plan.created_at.desc()).all()
    return render_template("es/dashboard/plans.html", plans=[p.to_dict() for p in plans])

@app.route("/dashboard/price-lists")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_price_lists():
    from app.models.master_scheme.price_list_model import PriceList
    price_lists = PriceList.query.order_by(PriceList.id.desc()).all()
    return render_template("es/dashboard/price_lists.html", price_lists=[pl.to_dict() for pl in price_lists])

@app.route("/dashboard/payments")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_payments():
    from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
    payments = PaymentTransaction.query.order_by(PaymentTransaction.createdAt.desc()).all()
    return render_template("es/dashboard/payments.html", payments=[p.to_dict() for p in payments])

@app.route("/dashboard/invoices")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_invoices():
    # Asumiendo que las facturas se manejan de alguna forma, por ahora lista vacía o fetch si existe el modelo
    # Si no hay modelo de facturas aún, podrías usar PaymentTransaction como base
    from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
    invoices = PaymentTransaction.query.filter(PaymentTransaction.status.in_(['SUCCESS', 'APPROVED'])).order_by(PaymentTransaction.createdAt.desc()).all()
    return render_template("es/dashboard/invoices.html", invoices=[i.to_dict() for i in invoices])

@app.route("/dashboard/ncf")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_ncf():
    return render_template("es/dashboard/ncf_sequences.html")

@app.route("/dashboard/ncf/logs")
@jwt_required()
@require_role(["ROOT", "SYS_ADMIN", "OWNER"])
def dashboard_ncf_logs():
    return render_template("es/dashboard/ncf_logs.html")

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

@app.post("/auth/reset-password")
def reset_password():
    from app.extensions import db
    try:
        data = request.json 
        token = data.get("token")
        password = data.get("password")

        user_id = verify_reset_token(token, max_age=3600)

        if user_id in (None, "expired"):
            return {"error": i18n._("auth.invalid_token")}, 400


        schema_name = get_user_scheme(user_id=user_id)
        print(schema_name)
        db.session.execute(
            text(f"SET search_path TO {schema_name}, public")
        )
        
        user = change_user_password(user_id=user_id, new_password=password)
        if not user:
            return {"error": i18n._("auth.user_not_found")}, 404

        return {"message": i18n._("auth.password_updated_success")}
    except ValueError as e:
        return {
            "success": False,
            "errors": e.args[0]
        }, 400

    except LookupError:
        return {
            "success": False,
            "message": i18n._("auth.user_not_found")
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
