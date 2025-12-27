from flask import  request, jsonify, render_template
from flask_jwt_extended import jwt_required
from ....extensions import db

from app.utils.helpers import send_email_template
from app import track_activity, require_role, audit_log
from app.utils.responses import success
from app.services.master_scheme.payment_service import request_suscription
from app.services.master_scheme.client_service import schema_exists, create_client_schema
from app.services.master_scheme.user_client_service import get_user_by_client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_model import User
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
import stripe
from app.utils.helpers import send_confirmation_account_email





@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
@audit_log(action="REQUEST_PAYMENT", resource_type="transacciones_pagos",description="request payment")
def request_payment(plan_identity):
   data = request_suscription(plan_identity=plan_identity)
   return success(data=data)



def payment_success():
    load_dotenv()
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    app_name = os.getenv("APP_NAME")
    session_id = request.args.get('session_id')
  
    # if not session_id:
    #     return redirect(url_for('home')) # O a tu página de precios

    # Intentamos buscar la transacción
    transaction = PaymentTransaction.query.filter_by(externalReference=session_id).first()
    
    # Si la transacción existe pero aún está "PENDING", es que el webhook no ha llegado.
    # En lugar de fallar, mostramos la vista de "Procesando" que haga un refresh automático.
    if not transaction or transaction.status == "PENDING":
        return render_template("es/processing_payment.html", 
                               app_name=app_name, 
                               session_id=session_id)

    if transaction.status == "APPROVED":
        
        client = Client.query.get(transaction.clientId)
        client_plan = ClientPlan.query.filter_by(client_id=client.clientId)
        user = get_user_by_client(client.uuid)
        
        # 2. ENVIAR EMAIL (Solo si el usuario está inactivo o no ha seteado clave)
        # Esto evita que se re-envíe si el usuario refresca la página de éxito
        if user and not user.user.isActive:
            send_confirmation_account_email(user.user.userId, client.contactName, user.user.email)
        
        invoice = Invoice.query.filter_by(transactionId=transaction.id).first()
        is_trial = (transaction.amount == 0)
        
        # Obtenemos el nombre del plan desde la relación si la tienes
        plan_name = "client_plan.plan.name"
        # if transaction.clientPlan:
        #     plan_name = transaction.clientPlan.plan.name

        # Usamos la nueva vista estética que diseñamos
        return render_template(
            "es/receipt_view.html", # Tu nueva plantilla estilo Stripe
            transaction=transaction,
            invoice=invoice,
            app_name=app_name,
            is_trial=is_trial,
            plan_name=plan_name,
            user_email=user.user.email # Pasamos el email para mostrarlo en el texto
        )
        
    return render_template("es/error_payment.html", app_name=app_name)

def payment_success_old():
    load_dotenv()
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    app_name = os.getenv("APP_NAME")
    session_id = request.args.get('session_id')
  
    # Buscamos la transacción
    transaction = PaymentTransaction.query.filter_by(externalReference=session_id).first()
    
    if transaction and transaction.status == "APPROVED":
        # Obtenemos la factura
        invoice = Invoice.query.filter_by(transactionId=transaction.id).first()
        
        # VALIDACIÓN DE TRIAL: 
        # Si el monto es 0, es un inicio de prueba
        if invoice:
            is_trial = (transaction.amount == 0)
            
            return render_template(
                "es/receipt_view.html",
                transaction=transaction,
                invoice=invoice,
                app_name=app_name,
                is_trial=is_trial, # <-- Pasamos esta variable al HTML
                plan_name="Plan name"
            )
        
    # Manejo de espera (el webhook de Stripe a veces tarda milisegundos más que la redirección)
    return render_template("es/processing_payment.html", app_name=app_name)


# def payment_cancel():
#     return "<h1>Pago Cancelado</h1><p>No se realizó ningún cargo. Puedes intentarlo de nuevo cuando quieras.</p>"



def payment_cancel():
    order_id = request.args.get('order_id')
    
    if order_id:
        try:
            # 1. Buscar la transacción por su referencia interna
            transaction = PaymentTransaction.query.filter_by(internalReference=order_id).first()
            
            if transaction and transaction.status == "PENDING":
                # 2. Cambiar el estado a CANCELLED
                transaction.status = "CANCELLED"
                db.session.commit()
                print(f"✅ Orden {order_id} marcada como cancelada por el usuario.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al cancelar la orden: {e}")

    # 3. Redirigir a una página de feedback o al login
    # Puedes usar el template 'payment_cancelled.html' que mencionamos antes
    return render_template("es/payment_cancelled.html", order_id=order_id)


def stripe_webhook():
    load_dotenv()
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    app_name = os.getenv("APP_NAME")
    
   
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # CASO 1: PAGO INICIAL (CHECKOUT)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        stripe_session_id = session.get('id')
        
        # En Checkout, el monto total nos dice si es Trial
        # amount_total es 0 si es un inicio de periodo de prueba
        is_trial = (session.get('amount_total') == 0)
        

        transaction = PaymentTransaction.query.filter_by(externalReference=stripe_session_id).first()
        if transaction:
            transaction.rawResponse = session
            process_successful_payment(transaction, session, app_name, is_trial=is_trial)
            

    # CASO 2: COBROS RECURRENTES AUTOMÁTICOS (MES 2, 3...)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice_data = event['data']['object']
  
        # Si es el pago de una suscripción
        subscription_id = (
                invoice_data.get('subscription') or 
                invoice_data.get('parent', {}).get('subscription_details', {}).get('subscription')
            )
            
        # En Invoice, amount_paid nos dice si este ciclo fue gratuito
        is_trial = (invoice_data.get('amount_paid') == 0)
        
        print(f"DEBUG: Subscription ID encontrado -> {subscription_id}")
        
        stripe_paid_at = invoice_data.get('status_transitions', {}).get('paid_at') or invoice_data.get('created')
        
        # Convertir el timestamp de Stripe a datetime con zona horaria UTC
        payment_date_dt = datetime.fromtimestamp(stripe_paid_at, tz=timezone.utc)
        
        
        # Si quieres guardar también el inicio y fin del periodo pagado
        period_start = datetime.fromtimestamp(invoice_data['lines']['data'][0]['period']['start'], tz=timezone.utc)
        period_end = datetime.fromtimestamp(invoice_data['lines']['data'][0]['period']['end'], tz=timezone.utc)

            
        if subscription_id:
            # Buscamos la transacción anterior para identificar al cliente/plan
            # Buscamos en el JSON rawResponse de transacciones previas
            prev_trans = PaymentTransaction.query.filter(
                PaymentTransaction.rawResponse['subscription'].astext == subscription_id
            ).first()

            if prev_trans:
                # Creamos una NUEVA transacción para el nuevo periodo
                new_trans = PaymentTransaction(
                    clientPlanId=prev_trans.clientPlanId,
                    clientId=prev_trans.clientId,
                    internalReference=f"REC-{int(datetime.now().timestamp())}",
                    externalReference=invoice_data.get('payment_intent'), # ID del cobro actual
                    amount=invoice_data.get('amount_paid') / 100,
                    currency=invoice_data.get('currency').upper(),
                    status="APPROVED",
                    paymentDate=payment_date_dt,
                    rawResponse=invoice_data
                )
                db.session.add(new_trans)
                db.session.flush() # Para obtener el ID de la transacción
                
                process_successful_payment(new_trans, invoice_data, app_name, is_trial)

    return jsonify({"status": "success"}), 200

# Función auxiliar para evitar repetir código de factura y email
def process_successful_payment(transaction, stripe_obj, app_name, is_trial):
    # 1. Actualizar/Confirmar Transacción
    transaction.status = "APPROVED"
    transaction.rawResponse = stripe_obj
    

    stripe_paid_at = stripe_obj.get('status_transitions', {}).get('paid_at') or stripe_obj.get('created')
    payment_date_dt = datetime.fromtimestamp(stripe_paid_at, tz=timezone.utc)
        
        
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

        
        client = Client.query.get(client_plan.client_id)
        if client:
            client.isActive = True
            
            # --- CREACIÓN DE ESQUEMA (Base de Datos separada) ---
            if not schema_exists(client.schemaName):
                create_client_schema(client.schemaName)
            
            # --- ACTIVACIÓN DE USUARIO Y ENVÍO DE CLAVE ---
            user = User.query.filter_by(idcliente=client.clientId).first()
            if user:
                user.active = True
                db.session.flush() # Asegura que tenemos los datos del usuario listos
                
                # ENVIAR EMAIL DE CONFIGURACIÓN DE CLAVE (Solo la primera vez/Trial)
                #if is_trial:
                    # Aquí asumo que esta función genera el token y envía el link de password
                    # send_confirmation_account_email(user.userId, client.contactName, user.email)
   
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
                app_name=app_name
            )
    except Exception as e:
        print(f"Error enviando email: {e}")