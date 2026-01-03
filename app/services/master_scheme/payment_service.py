
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_model import User
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.services.master_scheme.session_service import close_all_session
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.services.master_scheme.client_plan_service import  get_active_pending
from app.models.master_scheme.client_model import Client
from datetime import datetime, timezone
from app.services.master_scheme.payment_factory import get_current_provider
from ...extensions import db


from app.utils.helpers import send_email_template
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy import text
import stripe
import os


# @app.route('/api/v1/billing/portal-session', methods=['GET'])
# def create_portal_session():
#     # 1. Obtener el cliente logueado (ejemplo usando Flask-Login)
#     # Debes identificar qué cliente está intentando entrar
#     client = Client.query.filter_by(admin_id=current_user.id).first()

#     if not client or not client.stripe_customer_id:
#         return "No se encontró un perfil de facturación activo.", 404

#     try:
#         # 2. Le pedimos a Stripe una URL para este cliente específico
#         portal_session = stripe.billing_portal.Session.create(
#             customer=client.stripe_customer_id,
#             return_url=f"{request.host_url}dashboard", # A donde vuelve el usuario al terminar
#         )
        
#         # 3. Redirigimos al usuario a la página segura de Stripe
#         return redirect(portal_session.url)
#     except Exception as e:
#         return str(e), 500


def drop_schema(schema_name: str):
    """
    Elimina un esquema PostgreSQL de forma segura.
    """
    stmt = text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
    db.session.execute(stmt)
    db.session.commit()
  
  

def schema_exists(schema_name: str) -> bool:
    """
    Verifica si un esquema existe en la base de datos PostgreSQL.
    """
    query = text("""
        SELECT EXISTS(
            SELECT 1 
            FROM information_schema.schemata 
            WHERE schema_name = :schema
        )
    """)
    result = db.session.execute(query, {"schema": schema_name}).scalar()
    return bool(result)


def create_client_schema(new_schema: str, base_schema: str = "cliente"):
    sql = f"""
    CREATE SCHEMA IF NOT EXISTS {new_schema};

    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN 
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = '{base_schema}'
        LOOP
            EXECUTE format(
                'CREATE TABLE {new_schema}.%I (LIKE {base_schema}.%I INCLUDING ALL)',
                r.tablename,
                r.tablename
            );
        END LOOP;
    END $$;
    """
    db.session.execute(text(sql))

def request_suscription(plan_identity, billing_cycle="month") -> dict:
    provider = get_current_provider()
    
    try:
        # 1. Obtener datos del plan
        plan_del_cliente = get_active_pending(id=plan_identity)
        if not plan_del_cliente:
            return {"status": "error", "message": "Plan no encontrado"}

        client_id = plan_del_cliente.client_id
        # Cambiamos la forma de consultar para asegurar que esté en la sesión actual
        client = db.session.get(Client, client_id) 

        # 2. Datos de precios
        price_info = plan_del_cliente.price_list
        amount = float(price_info.price)
        currency = price_info.currency
        is_trial = price_info.is_trial
        trial_days = price_info.trial_days

        # 3. Crear transacción PENDING
        order_id = f"ORDER-{int(datetime.now(timezone.utc).timestamp())}"
        
        new_trans = PaymentTransaction(
            clientPlanId=plan_identity,
            clientId=client_id,
            amount=0 if is_trial else amount,
            currency=currency,
            internalReference=order_id,
            status="PENDING",
        )
        db.session.add(new_trans)
        db.session.commit()

        # 4. LLAMAR A STRIPE con bloque Try específico
        try:
        

            stripe_session = provider.create_checkout(
                client_id=client.clientId,
                amount=amount,
                currency=currency,
                order_id=order_id,
                client_email=client.billingEmail,
                plan_period=billing_cycle,
                is_trial_plan=is_trial, 
                trial_days=trial_days
            )
            
            if stripe_session and 'url' in stripe_session:
                new_trans.externalReference = stripe_session['external_id']
                db.session.commit()
                return {
                    "status": "success",
                    "checkout_url": stripe_session['url'],
                    "stripe_id": stripe_session['external_id']
                }
            else:
                raise Exception("Stripe no devolvió una URL válida")

        except Exception as stripe_err:
            # Si falla Stripe, marcamos la transacción como fallida
            new_trans.status = "FAILED"
            db.session.commit()
            print(f"❌ ERROR EN STRIPE PROVIDER: {str(stripe_err)}")
            return {"status": "error", "message": f"Error en Stripe: {str(stripe_err)}"}

    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR GENERAL EN REQUEST_SUSCRIPTION: {str(e)}")
        return {"status": "error", "message": str(e)}
    






    
def send_goodbye_email(client_email, contact_name, business_name):
    load_dotenv()
    base_url=os.getenv("BASE_URL")
    try:
        send_email_template(
            subject="Tu suscripción a Akdmia ha finalizado",
            to=[client_email],
            path_template="emails/es/subscription_ended.html",
            name=contact_name,
            business_name=business_name,
            reactivate_url=f"{base_url}/login"
        )
        print(f"Correo de despedida enviado a {client_email}")
    except Exception as e:
        print(f"Error enviando email de despedida: {str(e)}")
             
def process_successful_payment(transaction, stripe_obj, app_name, is_trial, commit=True):
    # 1. Actualizar/Confirmar Transacción
    transaction.status = "APPROVED"
    transaction.rawResponse = stripe_obj
    

    stripe_paid_at = stripe_obj.get('status_transitions', {}).get('paid_at') or stripe_obj.get('created')
    payment_date_dt = datetime.fromtimestamp(stripe_paid_at, tz=timezone.utc)
    # 1. Obtenemos los IDs de Stripe
    stripe_sub_id = stripe_obj.get('subscription') # Aquí viene el sub_xxx
    stripe_cus_id = stripe_obj.get('customer')     # Aquí viene el cus_xxx    
        
        

    transaction.paymentDate = payment_date_dt
    
    # 2. Crear Factura
    num_factura = f"FAC-{datetime.now().year}-{transaction.id}"
    new_invoice = Invoice(
        transactionId=transaction.id,
        invoiceNumber=num_factura,
        totalAmount=transaction.amount,
        issueDate=payment_date_dt
    )
    db.session.add(new_invoice)
    
    # 3. Extender vigencia del Plan
    client_plan = ClientPlan.query.get(transaction.clientPlanId)
    if client_plan:
        client_plan.status = "ACTIVE" # Asegúrate que el nombre de columna sea correcto

        
    client = Client.query.get(transaction.clientId)
    if client:
        client.isActive = True
        client.stripe_customer_id = stripe_cus_id
        if stripe_sub_id:
            client.stripe_subscription_id = stripe_sub_id
        
        # --- CREACIÓN DE ESQUEMA (Base de Datos separada) ---
        if not schema_exists(client.schemaName):
            create_client_schema(client.schemaName)
        
        # --- ACTIVACIÓN DE USUARIO Y ENVÍO DE CLAVE ---
        relacion = UsuarioCliente.query.filter_by(client_uuid=client.uuid).first()
        user = User.query.get(relacion.user_id)
        if user:
            user.isActive = True
            #db.session.flush() # Asegura que tenemos los datos del usuario listos
            
            # ENVIAR EMAIL DE CONFIGURACIÓN DE CLAVE (Solo la primera vez/Trial)
            #if is_trial:
                # Aquí asumo que esta función genera el token y envía el link de password
                # send_confirmation_account_email(user.userId, client.contactName, user.email)
    db.session.flush()
    if commit:
        db.session.commit()

    # 4. Enviar Email
    try:
        # En invoice.payment_succeeded el email está en customer_email
        email_to = stripe_obj.get('customer_email') or stripe_obj.get('customer_details', {}).get('email')
        name_to = stripe_obj.get('customer_name') or stripe_obj.get('customer_details', {}).get('name') or "Cliente"
        plan_name = client_plan.plan.code if client_plan else "Suscripción"

        if is_trial:
            d_fin = payment_date_dt + timedelta(days=client_plan.price_list.trial_days)
            # CASO TRIAL: Email de bienvenida a la prueba gratuita
            send_email_template(
                subject=f"¡Bienvenido a tu prueba gratuita de {plan_name} en {app_name}!",
                to=[email_to],
                path_template="emails/es/trial_welcome.html", # Template específico
                name=name_to,
                plan_name=plan_name,
                trial_end_date=d_fin.strftime('%d/%m/%Y'),
                app_name=app_name
            )
        else:
                        # --- AQUÍ OBTIENES LAS URL ---
            invoice_url = stripe_obj.get('hosted_invoice_url')
            # pdf_url = stripe_obj.get('invoice_pdf')
            # customer_email = stripe_obj.get('customer_email')
            # order_id = stripe_obj.get('metadata', {}).get('order_id') # Si lo pasaste en metadata
            
            # CASO PAGO REAL: Email de factura normal
            send_email_template(
                subject=f"Tu Factura {num_factura} - {app_name}",
                to=[email_to],
                path_template="emails/es/invoice_ready.html",
                name=name_to,
                invoice_num=num_factura,
                amount=float(transaction.amount),
                currency=transaction.currency,
                plan_name=plan_name,
                app_name=app_name,
                invoice_url = invoice_url
            )

    except Exception as e:
        print(f"Error enviando email: {e}")
        
def handle_checkout_session_completed(session, app_name):
    stripe_session_id = session.get('id')
    is_trial = (session.get('amount_total') == 0)
    
    transaction = PaymentTransaction.query.filter_by(externalReference=stripe_session_id).first()
    if transaction:
        transaction.rawResponse = session
        process_successful_payment(transaction, session, app_name, is_trial=is_trial)

def handle_invoice_payment_failed(invoice, app_name):
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    customer_id = invoice['customer']
    payment_intent_id = invoice.get('payment_intent')
    failure_msg = "Rechazo general por parte del banco"
    
    if payment_intent_id:
        pi = stripe.PaymentIntent.retrieve(payment_intent_id)
        if pi.last_payment_error:
            failure_msg = pi.last_payment_error.message
    
    client = Client.query.filter_by(stripe_customer_id=customer_id).first()
    if client:
        plan = ClientPlan.query.filter_by(client_id=client.clientId, status='ACTIVE').first()
        if plan:
            plan.status = 'PAST_DUE'
            db.session.commit()

        send_email_template(
            subject="Acción requerida: Error en el pago de tu suscripción",
            to=[client.billingEmail],
            path_template="emails/es/payment_failed.html",
            name=client.contactName,
            app_name=app_name,
            plan_name=plan.plan.name if plan else "Suscripción Akdmia",
            amount=invoice['amount_due'] / 100,
            currency=invoice['currency'].upper(),
            failure_reason=failure_msg,
            update_payment_url=f"{base_url}billing/settings"
        )

def handle_invoice_paid(invoice_data, app_name):
    try:
        subscription_id = (
            invoice_data.get('subscription') or 
            invoice_data.get('parent', {}).get('subscription_details', {}).get('subscription')
        )
        
        # También obtenemos el Customer ID 
        customer_id = invoice_data.get('customer')
        
        is_trial = (invoice_data.get('amount_paid') == 0)
        stripe_paid_at = invoice_data.get('status_transitions', {}).get('paid_at') or invoice_data.get('created')
        payment_date_dt = datetime.fromtimestamp(stripe_paid_at, tz=timezone.utc)
        
        if subscription_id:
            prev_trans = PaymentTransaction.query.filter(
                PaymentTransaction.rawResponse['subscription'].astext == subscription_id
            ).first()

            if prev_trans:
                print(f"prev_trans clientId : {prev_trans.clientId}")
                # --- ACTUALIZACIÓN DEL CLIENTE ---
                client = Client.query.get(prev_trans.clientId)
                if client:
                    # Si el campo sidcontratostripe está vacío, lo llenamos                
                    #if hasattr(client, 'stripe_subscription_id') and not client.stripe_subscription_id:
                    
                    print(f"Actualiza la suscripcion del cliente : {client.clientId}")
                    client.stripe_subscription_id = subscription_id
                    
                    # Aprovechamos para guardar el customer_id si no existe
                    # (Asumiendo que tienes una columna para ello, ej: stripe_customer_id)
                    if hasattr(client, 'stripe_customer_id') and not client.stripe_customer_id:
                        client.stripe_customer_id = customer_id
                    
                    db.session.flush() 
                # --------------------------------------------------
                
                new_trans = PaymentTransaction(
                    clientPlanId=prev_trans.clientPlanId,
                    clientId=prev_trans.clientId,
                    internalReference=f"REC-{int(datetime.now().timestamp())}",
                    externalReference=invoice_data.get('payment_intent'),
                    amount=invoice_data.get('amount_paid') / 100,
                    currency=invoice_data.get('currency').upper(),
                    status="APPROVED",
                    paymentDate=payment_date_dt,
                    rawResponse=invoice_data
                )
                db.session.add(new_trans)
                db.session.flush()
                process_successful_payment(new_trans, invoice_data, app_name, is_trial, commit=False)
                db.session.commit()
        
    except Exception as e:
            db.session.rollback()
            print(f"Error procesando el pago, se hizo rollback: {e}")
            raise e    

def handle_subscription_updated(subscription):
    stripe_cus_id = subscription['customer']
    client = Client.query.filter_by(stripe_customer_id=stripe_cus_id).first()
    
    if client:
        #client_plan = ClientPlan.query.filter_by(client_id=client.clientId, status='CANCELED').first()
        client_plan = ClientPlan.query.filter(
            ClientPlan.client_id == client.clientId, 
            ClientPlan.status != 'CANCELED'
        ).first()
        if client_plan:
            #new_end_date = datetime.fromtimestamp(subscription['current_period_end']).date()
            #client_plan.end_date = new_end_date
            
            stripe_status = subscription['status']
            client_plan.status = stripe_status.upper()
            print(client)
            print(stripe_status)
            # if stripe_status == 'active':
            #     client_plan.status = 'ACTIVE'
            # elif stripe_status in ['past_due', 'unpaid']:
            #     client_plan.status = 'PAST_DUE'
            
            db.session.commit()

def handle_subscription_deleted(subscription):
    print("handle_subscription_deleted")
    stripe_cus_id = subscription['customer']
    client = Client.query.filter_by(stripe_customer_id=stripe_cus_id).first()
    
    if client:
        client_plan = ClientPlan.query.filter_by(client_id=client.clientId).filter(
            ClientPlan.status.in_(['ACTIVE', 'PAST_DUE', 'TRIAL'])
        ).first()

        if client_plan:
            client_plan.status = 'CANCELED'
            client_plan.end_date = datetime.now().date() 

            user_ids_subquery = db.session.query(UsuarioCliente.user_id).filter(
                UsuarioCliente.client_uuid == client.uuid
            ).subquery()
            
            User.query.filter(User.userId.in_(user_ids_subquery)).update(
                {"isActive": False}, synchronize_session=False
            )
    
            users_to_close = User.query.filter(User.userId.in_(user_ids_subquery)).all()
            for u in users_to_close:
                close_all_session(user_id=u.userId, commit=False)
            
            #inactivo al cliente
            client.isActive = False
            
            db.session.commit()
            send_goodbye_email(client.billingEmail, client.contactName, business_name=client.businessName)
                       
def handle_subscription_trial_will_end(subscription, app_name):
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    stripe_cus_id = subscription['customer']
    
    # 1. Buscar al cliente
    client = Client.query.filter_by(stripe_customer_id=stripe_cus_id).first()
    
    if client:
        # 2. Obtener la fecha exacta en la que se hará el cobro
        trial_end_date = datetime.fromtimestamp(subscription['trial_end']).date()
        client_plan = ClientPlan.query.filter_by(client_id=client.clientId, status='ACTIVE').first()
        plan_name = client_plan.plan.code if client_plan else "Suscripción"
        
        # 3. Enviar email recordatorio
        send_email_template(
            subject=f"Tu periodo de prueba en {app_name} termina pronto",
            to=[client.billingEmail],
            path_template="emails/es/trial_ending.html",
            name=client.contactName,
            business_name=client.businessName,
            trial_end_date=trial_end_date.strftime('%d/%m/%Y'),
            plan_name=plan_name,
            update_payment_url=f"{base_url}billing/portal-session" # El portal que creamos
        )
        print(f"🔔 Aviso de fin de trial enviado a: {client.businessName}")