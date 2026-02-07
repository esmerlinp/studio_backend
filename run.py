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
from app.api.v1.master.country.routes import country_bp
from app.api.v1.master.logs_webhooks.routes import logs_webhooks_bp
from app.api.v1.master.modules.routes import modules_bp
from app.api.v1.master.currencies.routes import currencies_bp
from app.api.v1.master.month_names.routes import month_names_bp
from app.api.v1.master.weekday_names.routes import weekday_names_bp
from app.api.v1.master.other_schools.routes import other_schools_bp
from app.api.v1.master.ncf.routes import ncf_bp
from app.api.v1.master.allergies.routes import allergies_bp
from app.api.v1.master.banks.routes import banks_bp
from app.api.v1.master.cities.routes import cities_bp
from app.api.v1.master.marital_status.routes import marital_status_bp
from app.api.v1.master.functionalities.routes import functionalities_bp
from app.api.v1.master.functions.routes import functions_bp
from app.api.v1.master.medical_institutions.routes import medical_institutions_bp
from app.api.v1.master.health_insurance_institutions.routes import health_insurance_institutions_bp
from app.api.v1.base.roles.routes import roles_bp
from app.api.v1.master.screens.routes import screens_bp
from app.api.v1.master.screen_functionalities.routes import screen_functionalities_bp
from app.api.v1.master.payment_processors.routes import payment_processors_bp
from app.api.v1.master.professions.routes import professions_bp
from app.api.v1.master.role_permissions.routes import role_permissions_bp
from app.api.v1.master.genders.routes import genders_bp
from app.api.v1.master.attendance_types.routes import attendance_types_bp
from app.api.v1.master.document_types.routes import document_types_bp
from app.api.v1.master.blood_types.routes import blood_types_bp
from app.api.v1.master.phone_types.routes import phone_types_bp
from app.api.v1.master.roles.routes import roles_bp as master_roles_bp
from app.api.v1.master.sectors.routes import sectors_bp
from app.api.v1.master.search.controller import search_bp
from app.api.v1.master.chatbot.routes import chatbot_bp
from app.api.v1.client_scheme.active_cycle_courses.routes import active_cycle_courses_bp
from app.api.v1.client_scheme.active_cycle_attendances.routes import active_cycle_attendances_bp
from app.api.v1.client_scheme.active_cycle_competencies.routes import active_cycle_competencies_bp
from app.api.v1.client_scheme.schedule_block_details.routes import schedule_block_details_bp
from app.api.v1.client_scheme.student_charge_balances.routes import student_charge_balances_bp
from app.api.v1.client_scheme.active_cycle_students.routes import active_cycle_students_bp
from app.api.v1.client_scheme.current_taxes.routes import current_taxes_bp
from app.api.v1.client_scheme.subject_areas.routes import subject_areas_bp
from app.api.v1.client_scheme.subjects.routes import subjects_bp
from app.api.v1.client_scheme.attendances.routes import attendances_bp
from app.api.v1.client_scheme.schedule_blocks.routes import schedule_blocks_bp
from app.api.v1.client_scheme.payment_calendar.routes import payment_calendar_bp
from app.api.v1.client_scheme.cycles.routes import cycles_bp
from app.api.v1.client_scheme.cycle_level_schedule_blocks.routes import cycle_level_schedule_blocks_bp
from app.api.v1.client_scheme.competencies.routes import competencies_bp
from app.api.v1.client_scheme.concepts.routes import concepts_bp
from app.api.v1.client_scheme.courses.routes import courses_bp
from app.api.v1.client_scheme.child_discounts.routes import child_discounts_bp
from app.api.v1.client_scheme.students.routes import students_bp
from app.api.v1.client_scheme.evaluation_requests.routes import evaluation_requests_bp
from app.api.v1.client_scheme.formulas.routes import formulas_bp
from app.api.v1.client_scheme.payment_frequencies.routes import payment_frequencies_bp
from app.api.v1.client_scheme.taxes.routes import taxes_bp
from app.api.v1.client_scheme.inscriptions.routes import inscriptions_bp
from app.api.v1.client_scheme.levels.routes import levels_bp
from app.api.v1.client_scheme.grade_corrections.routes import grade_corrections_bp
from app.api.v1.client_scheme.partials.routes import partials_bp
from app.api.v1.client_scheme.cycle_partials.routes import cycle_partials_bp
from app.api.v1.client_scheme.surcharges_per_day.routes import surcharges_per_day_bp
from app.api.v1.client_scheme.requests.routes import requests_bp
from app.api.v1.client_scheme.sub_cycles.routes import sub_cycles_bp
from app.api.v1.client_scheme.active_cycle_grade_corrections.routes import active_cycle_grade_corrections_bp
from app.api.v1.client_scheme.active_cycle_student_grades.routes import active_cycle_student_grades_bp
from app.api.v1.client_scheme.school_payments.routes import school_payments_bp
from app.api.v1.client_scheme.sub_cycle_course_competencies.routes import sub_cycle_course_competencies_bp
from app.api.v1.client_scheme.payments.routes import payments_bp
from app.services.master_scheme.user_service import change_user_password, get_user_scheme, get_user_by_id
from app import create_app, require_role, require_permission
from app.utils import i18n
from app.utils.helpers import verify_reset_token
from app.utils.responses import error
import os
from dotenv import load_dotenv
from app.extensions import db
from sqlalchemy import text, or_
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
app.register_blueprint(country_bp)
app.register_blueprint(logs_webhooks_bp)
app.register_blueprint(modules_bp)
app.register_blueprint(currencies_bp)
app.register_blueprint(month_names_bp)
app.register_blueprint(weekday_names_bp)
app.register_blueprint(other_schools_bp)
app.register_blueprint(allergies_bp)
app.register_blueprint(banks_bp)
app.register_blueprint(cities_bp)
app.register_blueprint(marital_status_bp)
app.register_blueprint(functionalities_bp)
app.register_blueprint(functions_bp)
app.register_blueprint(medical_institutions_bp)
app.register_blueprint(health_insurance_institutions_bp)
app.register_blueprint(screens_bp)
app.register_blueprint(screen_functionalities_bp)
app.register_blueprint(payment_processors_bp)
app.register_blueprint(professions_bp)
app.register_blueprint(role_permissions_bp)
app.register_blueprint(genders_bp)
app.register_blueprint(attendance_types_bp)
app.register_blueprint(document_types_bp)
app.register_blueprint(blood_types_bp)
app.register_blueprint(phone_types_bp)
app.register_blueprint(master_roles_bp)
app.register_blueprint(sectors_bp)
app.register_blueprint(search_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(active_cycle_courses_bp)
app.register_blueprint(active_cycle_attendances_bp)
app.register_blueprint(active_cycle_competencies_bp)
app.register_blueprint(schedule_block_details_bp)
app.register_blueprint(student_charge_balances_bp)
app.register_blueprint(active_cycle_students_bp)
app.register_blueprint(current_taxes_bp)
app.register_blueprint(subject_areas_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(attendances_bp)
app.register_blueprint(schedule_blocks_bp)
app.register_blueprint(payment_calendar_bp)
app.register_blueprint(cycles_bp)
app.register_blueprint(cycle_level_schedule_blocks_bp)
app.register_blueprint(competencies_bp)
app.register_blueprint(concepts_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(child_discounts_bp)
app.register_blueprint(students_bp)
app.register_blueprint(payments_bp)

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
    "countries.get_countries",
    "dashboard_login"
}



@app.route('/health')
def health():
    from flask_limiter.util import get_remote_address
    get_remote_address()
    return f'OK - {get_remote_address()}', 200
           


@app.route("/logout")
def logout_dashboard():
    from flask_jwt_extended import unset_jwt_cookies
    response = redirect("/dashboard/login")
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
        
        # Redireccionar al login correspondiente
        if request.path.startswith('/dashboard'):
            return redirect('/dashboard/login')
        
        # Si es /client o cualquier otro, va al login del main
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

@app.route("/dashboard/login")
def dashboard_login():
    return render_template("es/dashboard/login.html")

@app.route("/dashboard")
@jwt_required()
@require_permission("SC_DASHBOARD", "CONSULTAR")
def dashboard():
    from app.services.master_scheme.dashboard_service import get_admin_dashboard_data
    data = get_admin_dashboard_data()
    return render_template("es/dashboard.html", 
                         stats=data.get('stats'), 
                         recent_clients=data.get('recent_clients'), 
                         recent_payments=data.get('recent_payments'))

@app.route("/dashboard/clients")
@jwt_required()
@require_permission("SC_CLIENTES", "CONSULTAR")
def dashboard_clients():
    from app.models.master_scheme.client_model import Client
    from app.models.master_scheme.client_model import Client
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'clientId')
    order = request.args.get('order', 'desc')

    query = Client.query

    if search_query:
        query = query.filter(or_(
            Client.name.ilike(f'%{search_query}%'),
            Client.businessName.ilike(f'%{search_query}%'),
            Client.documentNumber.ilike(f'%{search_query}%'),
            Client.contactName.ilike(f'%{search_query}%')
        ))

    # Validate sort column to prevent injection/errors
    valid_sort_cols = {
        'clientId': Client.clientId,
        'name': Client.name,
        'businessName': Client.businessName,
        'createdAt': Client.createdAt,
        'isActive': Client.isActive
    }
    
    sort_col = valid_sort_cols.get(sort_by, Client.clientId)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/clients.html", clients=pagination.items, pagination=pagination)

@app.route("/dashboard/clients/<int:clientId>")
@jwt_required()
@require_permission("SC_CLIENTES", "CONSULTAR")
def dashboard_client_details(clientId):
    # We pass the ID and let the frontend fetch the details via API
    return render_template("es/dashboard/client_details.html", clientId=clientId)

@app.route("/dashboard/clients/create")
@jwt_required()
@require_permission("SC_CLIENTES", "CREAR")
def dashboard_create_client():
    return render_template("es/dashboard/create_client.html")

@app.route("/dashboard/plans")
@jwt_required()
@require_permission("SC_PLANES", "CONSULTAR")
def dashboard_plans():
    from app.models.master_scheme.plans_model import Plan
    from app.models.master_scheme.price_list_model import PriceList  # Required for relationship mapping
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')

    query = Plan.query

    if search_query:
        query = query.filter(or_(
            Plan.name.ilike(f'%{search_query}%'),
            Plan.code.ilike(f'%{search_query}%')
        ))
    
    valid_sort_cols = {
        'name': Plan.name,
        'code': Plan.code,
        'created_at': Plan.created_at,
        'status': Plan.is_active
    }
    
    sort_col = valid_sort_cols.get(sort_by, Plan.created_at)

    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/plans.html", plans=pagination.items, pagination=pagination)

@app.route("/dashboard/price-lists")
@jwt_required()
@require_permission("SC_LISTAS_DE_PRECIOS", "CONSULTAR")
def dashboard_price_lists():
    from app.models.master_scheme.price_list_model import PriceList
    from app.models.master_scheme.plans_model import Plan  # Ensure relationship loading
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = PriceList.query.order_by(PriceList.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/price_lists.html", price_lists=pagination.items, pagination=pagination)

@app.route("/dashboard/payments")
@jwt_required()
@require_permission("SC_PAGOS", "CONSULTAR")
def dashboard_payments():
    from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'createdAt')
    order = request.args.get('order', 'desc')

    query = PaymentTransaction.query

    if search_query:
        query = query.filter(or_(
            PaymentTransaction.internalReference.ilike(f'%{search_query}%'),
            PaymentTransaction.externalReference.ilike(f'%{search_query}%')
        ))

    valid_sort_cols = {
        'createdAt': PaymentTransaction.createdAt,
        'amount': PaymentTransaction.amount,
        'status': PaymentTransaction.status,
        'paymentDate': PaymentTransaction.paymentDate
    }

    sort_col = valid_sort_cols.get(sort_by, PaymentTransaction.createdAt)

    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/payments.html", payments=pagination.items, pagination=pagination)

@app.route("/dashboard/invoices")
@jwt_required()
@require_permission("SC_INVOICES", "CONSULTAR")
def dashboard_invoices():
    # Invoices (PaymentTransactions with SUCCESS/APPROVED status)
    from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'createdAt')
    order = request.args.get('order', 'desc')

    query = PaymentTransaction.query.filter(PaymentTransaction.status.in_(['SUCCESS', 'APPROVED']))

    if search_query:
        query = query.filter(or_(
            PaymentTransaction.internalReference.ilike(f'%{search_query}%'),
            PaymentTransaction.externalReference.ilike(f'%{search_query}%')
        ))

    valid_sort_cols = {
        'createdAt': PaymentTransaction.createdAt,
        'amount': PaymentTransaction.amount,
        'paymentDate': PaymentTransaction.paymentDate
    }
    
    sort_col = valid_sort_cols.get(sort_by, PaymentTransaction.createdAt)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/invoices.html", invoices=pagination.items, pagination=pagination)

@app.route("/dashboard/ncf")
@jwt_required()
@require_permission("SC_SECUENCIAS_NCF", "CONSULTAR")
def dashboard_ncf():
    return render_template("es/dashboard/ncf_sequences.html")

@app.route("/dashboard/ncf/logs")
@jwt_required()
@require_permission("SC_LOGS_NCF", "CONSULTAR")
def dashboard_ncf_logs():
    return render_template("es/dashboard/ncf_logs.html")

@app.route("/dashboard/allergies")
@jwt_required()
@require_permission("SC_ALERGIAS", "CONSULTAR")
def dashboard_allergies():
    from app.models.master_scheme.allergy_model import Allergy
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    query = Allergy.query

    if search_query:
        query = query.filter(Allergy.name.ilike(f'%{search_query}%'))

    valid_sort_cols = {
        'name': Allergy.name,
        'id': Allergy.id,
        'is_active': Allergy.is_active
    }
    
    sort_col = valid_sort_cols.get(sort_by, Allergy.name)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/allergies.html", allergies=pagination.items, pagination=pagination)

@app.route("/dashboard/banks")
@jwt_required()
@require_permission("SC_BANCOS", "CONSULTAR")
def dashboard_banks():
    from app.services.master_scheme.bank_service import get_banks
    banks = get_banks()
    return render_template("es/dashboard/banks.html", banks=[b.to_dict() for b in banks])

@app.route("/dashboard/cities")
@jwt_required()
@require_permission("SC_CIUDADES", "CONSULTAR")
def dashboard_cities():
    from app.models.master_scheme.city_model import City
    from app.models.master_scheme.country_model import Country
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    
    query = City.query.join(Country) # Ensure Country can be joined if needed

    if search_query:
        query = query.filter(or_(
            City.name.ilike(f'%{search_query}%'),
            Country.name.ilike(f'%{search_query}%')
        ))
        
    pagination = query.order_by(City.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Also fetch countries for the modal if needed, but usually APIs handle that.
    # If the template needs `countries` list for a dropdown:
    countries = Country.query.filter_by(is_active=True).order_by(Country.name.asc()).all()
    
    return render_template("es/dashboard/cities.html", cities=pagination.items, pagination=pagination, countries=countries)

@app.route("/dashboard/marital-status")
@jwt_required()
@require_permission("SC_ESTADOS_CIVILES", "CONSULTAR")
def dashboard_marital_status():
    from app.services.master_scheme.marital_status_service import get_marital_statuses
    statuses = get_marital_statuses()
    return render_template("es/dashboard/marital_status.html", statuses=[s.to_dict() for s in statuses])

@app.route("/dashboard/functionalities")
@jwt_required()
@require_permission("SC_FUNCIONALIDADES", "CONSULTAR")
def dashboard_functionalities():
    from app.models.master_scheme.functionality_model import Functionality
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    query = Functionality.query

    if search_query:
        query = query.filter(or_(
            Functionality.name.ilike(f'%{search_query}%'),
            Functionality.code.ilike(f'%{search_query}%')
        ))

    valid_sort_cols = {
        'name': Functionality.name,
        'code': Functionality.code,
        'is_active': Functionality.is_active
    }
    
    sort_col = valid_sort_cols.get(sort_by, Functionality.name)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/functionalities.html", functionalities=pagination.items, pagination=pagination)

@app.route("/dashboard/functions")
@jwt_required()
@require_permission("SC_FUNCIONES", "CONSULTAR")
def dashboard_functions():
    from app.services.master_scheme.function_service import get_functions
    funcs = get_functions()
    return render_template("es/dashboard/functions.html", functions=[f.to_dict() for f in funcs])

@app.route("/dashboard/medical-institutions")
@jwt_required()
@require_permission("SC_INSTITUCIONES_MÉDICAS", "CONSULTAR")
def dashboard_medical_institutions():
    from app.services.master_scheme.medical_institution_service import get_medical_institutions
    insts = get_medical_institutions()
    return render_template("es/dashboard/medical_institutions.html", institutions=[i.to_dict() for i in insts])

@app.route("/dashboard/health-insurance-institutions")
@jwt_required()
@require_permission("SC_ARS", "CONSULTAR")
def dashboard_health_insurance_institutions():
    from app.services.master_scheme.health_insurance_institution_service import get_health_insurance_institutions
    insts = get_health_insurance_institutions()
    return render_template("es/dashboard/health_insurance_institutions.html", institutions=[i.to_dict() for i in insts])

@app.route("/dashboard/logs-webhooks")
@jwt_required()
@require_permission("SC_LOGS_WEBHOOKS", "CONSULTAR")
def dashboard_logs_webhooks():
    from app.services.master_scheme.log_service import get_logs
    logs = get_logs()
    return render_template("es/dashboard/logs_webhooks.html", logs=[l.to_dict() for l in logs])

@app.route("/dashboard/modules")
@jwt_required()
@require_permission("SC_MÓDULOS", "CONSULTAR")
def dashboard_modules():
    from app.services.master_scheme.module_service import get_modules
    modules = get_modules()
    return render_template("es/dashboard/modules.html", modules=[m.to_dict() for m in modules])

@app.route("/dashboard/currencies")
@jwt_required()
@require_permission("SC_MONEDAS", "CONSULTAR")
def dashboard_currencies():
    from app.services.master_scheme.currency_service import get_currencies
    currencies = get_currencies()
    return render_template("es/dashboard/currencies.html", currencies=[c.to_dict() for c in currencies])

@app.route("/dashboard/month-names")
@jwt_required()
@require_permission("SC_NOMBRES_DE_MESES", "CONSULTAR")
def dashboard_month_names():
    from app.services.master_scheme.month_name_service import get_month_names
    months = get_month_names()
    return render_template("es/dashboard/month_names.html", months=[m.to_dict() for m in months])

@app.route("/dashboard/weekday-names")
@jwt_required()
@require_permission("SC_NOMBRES_DE_DÍAS", "CONSULTAR")
def dashboard_weekday_names():
    from app.services.master_scheme.weekday_name_service import get_weekday_names
    days = get_weekday_names()
    return render_template("es/dashboard/weekday_names.html", days=[d.to_dict() for d in days])

@app.route("/dashboard/other-schools")
@jwt_required()
@require_permission("SC_OTRAS_ESCUELAS", "CONSULTAR")
def dashboard_other_schools():
    from app.services.master_scheme.other_school_service import get_other_schools
    schools = get_other_schools()
    return render_template("es/dashboard/other_schools.html", schools=[s.to_dict() for s in schools])

@app.route("/dashboard/countries")
@jwt_required()
@require_permission("SC_COUNTRIES", "CONSULTAR")
def dashboard_countries():
    from app.models.master_scheme.country_model import Country
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    query = Country.query

    if search_query:
        query = query.filter(or_(
            Country.name.ilike(f'%{search_query}%'),
            Country.iso_code.ilike(f'%{search_query}%')
        ))

    valid_sort_cols = {
        'name': Country.name,
        'iso_code': Country.iso_code,
        'is_active': Country.is_active
    }
    
    sort_col = valid_sort_cols.get(sort_by, Country.name)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/countries.html", countries=pagination.items, pagination=pagination)

@app.route("/dashboard/users")
@jwt_required()
@require_permission("SC_USUARIOS", "CONSULTAR")
def dashboard_users():
    from app.models.master_scheme.user_model import User
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Optional: filter by ID if provided in query (for search redirection)
    user_id = request.args.get('id', type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'userId')
    order = request.args.get('order', 'desc')

    query = User.query
    if user_id:
        query = query.filter_by(userId=user_id)
    
    if search_query:
        query = query.filter(or_(
            User.username.ilike(f'%{search_query}%'),
            User.firstName.ilike(f'%{search_query}%'),
            User.lastName.ilike(f'%{search_query}%'),
            User.email.ilike(f'%{search_query}%')
        ))
        
    valid_sort_cols = {
        'userId': User.userId,
        'username': User.username,
        'firstName': User.firstName,
        'email': User.email,
        'rol': User.rol,
        'isActive': User.isActive
    }
    
    sort_col = valid_sort_cols.get(sort_by, User.userId)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/users.html", users=pagination.items, pagination=pagination)

# ------------------------------
# Client Environment Routes
# ------------------------------

@app.route("/client/dashboard")
@jwt_required()
def client_dashboard():
    return render_template("es/client/dashboard.html", active_page='dashboard')

@app.route("/client/admissions")
@jwt_required()
def client_admissions():
    return render_template("es/client/admissions.html", active_page='admissions')

@app.route("/client/students")
@jwt_required()
def client_students():
    return render_template("es/client/students.html", active_page='students')

@app.route("/client/config/cycles")
@jwt_required()
def client_config_cycles():
    return render_template("es/client/cycles.html", active_page='config_cycles')

@app.route("/client/attendance")
@jwt_required()
def client_attendance():
    return render_template("es/client/attendance.html", active_page='attendance')

@app.route("/client/config/courses")
@jwt_required()
def client_config_courses():
    return render_template("es/client/courses.html", active_page='config_courses')

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

# ------------------------------
# Batch 3 Dashboard Routes
# ------------------------------

@app.route("/dashboard/screens")
@jwt_required()
@require_permission("SC_PANTALLAS", "CONSULTAR")
def dashboard_screens():
    from app.models.master_scheme.screen_model import Screen
    from app.models.master_scheme.module_model import Module
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'order')
    order_mode = request.args.get('order', 'asc')

    query = db.session.query(
        Screen, Module
    ).join(Module, Screen.module_id == Module.id)

    if search_query:
        query = query.filter(or_(
            Screen.name.ilike(f'%{search_query}%'),
            Screen.route.ilike(f'%{search_query}%'),
            Module.name.ilike(f'%{search_query}%')
        ))

    # Sort logic
    valid_sort_cols = {
        'order': Screen.order,
        'name': Screen.name,
        'module': Module.name,
        'route': Screen.route,
        'is_active': Screen.is_active
    }
    sort_col = valid_sort_cols.get(sort_by, Screen.order)
    
    if order_mode == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("es/dashboard/screens.html", pagination=pagination)

@app.route("/dashboard/screen-functionalities")
@jwt_required()
@require_permission("SC_FUNCIONALIDADES_PANTALLA", "CONSULTAR")
def dashboard_screen_functionalities():
    from app.models.master_scheme.screen_functionality_model import ScreenFunctionality
    from app.models.master_scheme.screen_model import Screen
    from app.models.master_scheme.functionality_model import Functionality
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = db.session.query(
        ScreenFunctionality, Screen, Functionality
    ).join(Screen, ScreenFunctionality.screen_id == Screen.id
    ).join(Functionality, ScreenFunctionality.functionality_id == Functionality.id
    ).order_by(Screen.name.asc(), Functionality.name.asc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("es/dashboard/screen_functionalities.html", pagination=pagination)

@app.route("/dashboard/payment-processors")
@jwt_required()
@require_permission("SC_PROCESADORES_DE_PAGO", "CONSULTAR")
def dashboard_payment_processors():
    from app.services.master_scheme.payment_processor_service import get_payment_processors
    pp = get_payment_processors()
    return render_template("es/dashboard/payment_processors.html", processors=pp)

@app.route("/dashboard/professions")
@jwt_required()
@require_permission("SC_PROFESIONES", "CONSULTAR")
def dashboard_professions():
    from app.models.master_scheme.profession_model import Profession
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')

    query = Profession.query

    if search_query:
        query = query.filter(Profession.name.ilike(f'%{search_query}%'))

    valid_sort_cols = {
        'name': Profession.name,
        'is_active': Profession.is_active
    }
    
    sort_col = valid_sort_cols.get(sort_by, Profession.name)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/professions.html", professions=pagination.items, pagination=pagination)

@app.route("/dashboard/role-permissions")
@jwt_required()
@require_permission("SC_PERMISOS_DE_ROLES", "CONSULTAR")
def dashboard_role_permissions():
    from app.models.master_scheme.role_permission_model import RolePermission
    from app.models.master_scheme.roles_model import Role
    from app.models.master_scheme.screen_functionality_model import ScreenFunctionality
    from app.models.master_scheme.screen_model import Screen
    from app.models.master_scheme.functionality_model import Functionality

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = db.session.query(
        RolePermission, Role, Screen, Functionality
    ).join(Role, RolePermission.role_id == Role.id
    ).join(ScreenFunctionality, RolePermission.screen_functionality_id == ScreenFunctionality.id
    ).join(Screen, ScreenFunctionality.screen_id == Screen.id
    ).join(Functionality, ScreenFunctionality.functionality_id == Functionality.id
    ).order_by(Role.name.asc(), Screen.name.asc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("es/dashboard/role_permissions.html", pagination=pagination)

@app.route("/dashboard/genders")
@jwt_required()
@require_permission("SC_GÉNEROS", "CONSULTAR")
def dashboard_genders():
    from app.services.master_scheme.gender_service import get_genders
    g = get_genders()
    return render_template("es/dashboard/genders.html", genders=g)

@app.route("/dashboard/attendance-types")
@jwt_required()
@require_permission("SC_TIPOS_DE_ASISTENCIA", "CONSULTAR")
def dashboard_attendance_types():
    from app.services.master_scheme.attendance_type_service import get_attendance_types
    at = get_attendance_types()
    return render_template("es/dashboard/attendance_types.html", attendance_types=at)

@app.route("/dashboard/document-types")
@jwt_required()
@require_permission("SC_TIPOS_DE_DOCUMENTO", "CONSULTAR")
def dashboard_document_types():
    from app.services.master_scheme.document_type_service import get_document_types
    dt = get_document_types()
    return render_template("es/dashboard/document_types.html", document_types=dt)

@app.route("/dashboard/blood-types")
@jwt_required()
@require_permission("SC_TIPOS_DE_SANGRE", "CONSULTAR")
def dashboard_blood_types():
    from app.services.master_scheme.blood_type_service import get_blood_types
    bt = get_blood_types()
    return render_template("es/dashboard/blood_types.html", blood_types=bt)

@app.route("/dashboard/phone-types")
@jwt_required()
@require_permission("SC_TIPOS_DE_TELÉFONO", "CONSULTAR")
def dashboard_phone_types():
    from app.services.master_scheme.phone_type_service import get_phone_types
    pt = get_phone_types()
    return render_template("es/dashboard/phone_types.html", phone_types=pt)

@app.route("/dashboard/roles-master")
@jwt_required()
@require_permission("SC_ROLES", "CONSULTAR")
def dashboard_roles_master():
    from app.models.master_scheme.roles_model import Role
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Role.query.order_by(Role.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("es/dashboard/roles_master.html", roles=pagination.items, pagination=pagination)

@app.route("/dashboard/sectors")
@jwt_required()
@require_permission("SC_SECTORES", "CONSULTAR")
def dashboard_sectors():
    from app.services.master_scheme.sector_service import get_sectors
    s = get_sectors()
    return render_template("es/dashboard/sectors.html", sectors=s)

@app.route("/dashboard/user-roles")
@jwt_required()
@require_permission("SC_ROLES_DE_USUARIO", "CONSULTAR")
def dashboard_user_roles():
    from app.models.master_scheme.user_roles_model import UserRole
    from app.models.master_scheme.user_model import User
    from app.models.master_scheme.roles_model import Role
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = db.session.query(
        UserRole, User, Role
    ).join(User, UserRole.user_id == User.userId
    ).join(Role, UserRole.role_id == Role.id
    ).order_by(User.username.asc(), Role.name.asc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("es/dashboard/user_roles.html", pagination=pagination)

@app.route("/dashboard/user-sessions")
@jwt_required()
@require_permission("SC_SESIONES", "CONSULTAR")
def dashboard_user_sessions():
    from app.models.master_scheme.session_model import Session
    from app.models.master_scheme.user_model import User
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort_by', 'createAt')
    order = request.args.get('order', 'desc')
    
    query = db.session.query(
        Session, User
    ).join(User, Session.userId == User.userId)
    
    if search_query:
        query = query.filter(or_(
            User.username.ilike(f'%{search_query}%'),
            User.email.ilike(f'%{search_query}%'),
            Session.ipAddress.ilike(f'%{search_query}%')
        ))
        
    valid_sort_cols = {
        'createAt': Session.createAt,
        'ipAddress': Session.ipAddress,
        'username': User.username
    }
    sort_col = valid_sort_cols.get(sort_by, Session.createAt)
    
    if order == 'asc':
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("es/dashboard/user_sessions.html", pagination=pagination)

if __name__ == '__main__':
        
    #app.run(debug=True)
    # Usa la variable de entorno PORT si existe, de lo contrario 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

