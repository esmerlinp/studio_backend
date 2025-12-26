from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.helpers import send_email_template


from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.services.master_scheme.client_plan_service import get_active_plan
from app.services.master_scheme.client_service import get_client_by_id
from app.models.master_scheme.client_plans_model import ClientPlan
from flask import jsonify
import datetime
from app import db
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import stripe

from app.services.master_scheme.payment_factory import get_current_provider
from ....extensions import db
from app import track_activity, require_role, audit_log
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.utils.responses import success, error



@jwt_required()
@track_activity
@require_role(["SUPER_ADMIN", "SYS_ADMIN"])
@audit_log(action="REQUEST_PAYMENT", resource_type="transacciones_pagos",description="request payment")
def request_payment(plan_identity):
    # 1. Obtenemos el proveedor (Stripe según tu .env)
    provider = get_current_provider()
    plan_del_cliente = get_active_plan(id=plan_identity)

    client_id = plan_del_cliente.client_id
    client = get_client_by_id(clientId=client_id)

    amount = float(plan_del_cliente.price_list.price)
    #amount = 220.00
    currency =  plan_del_cliente.price_list.currency  #"DOP"

    # 3. CREAR TRANSACCIÓN EN TU DB (Estado inicial)
    # Generamos una referencia interna para Stripe
    order_id = f"ORDER-{int(datetime.now(timezone.utc).timestamp())}"
    
    new_trans = PaymentTransaction(
        clientPlanId=plan_identity,
        clientId=client_id,
        amount=amount,
        currency=currency,
        internalReference= order_id,
        status="PENDING"
    )
    db.session.add(new_trans)
    db.session.commit()

    # 4. LLAMAR A STRIPE
    # Pasamos el internal_ref para que Stripe nos lo devuelva en el webhook
    stripe_session = provider.create_checkout(
        amount=amount,
        currency=currency,
        order_id=order_id,
        client_email=client.billingEmail,
        plan_period="mensual"
    )

    if stripe_session:
        new_trans.externalReference = stripe_session['external_id'] # <--- El cs_test_...
        db.session.commit()
    
        data = {
            "status": "success",
            "checkout_url": stripe_session['url'],
            "stripe_id": stripe_session['external_id']
        }
        return success(data)

    
    return jsonify({"status": "error", "msg": "No se pudo crear la sesión"}), 500



def payment_success():
    # 1. Obtenemos el session_id de la URL
    load_dotenv()
        
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    app_name = os.getenv("APP_NAME")
    session_id = request.args.get('session_id')
    
    # Buscamos la transacción y su factura relacionada
    transaction = PaymentTransaction.query.filter_by(externalReference=session_id).first()
    
    if transaction and transaction.status == "APPROVED":
        # Obtenemos la factura generada en el webhook
        invoice = Invoice.query.filter_by(transactionId=transaction.id).first()
        
        return render_template(
            "es/receipt_view.html", # Tu vista de recibo
            transaction=transaction,
            invoice=invoice,
            app_name=app_name
        )
    
    # Si el webhook aún no procesó (raro pero posible), mostramos espera
    return "<h1>Estamos procesando tu recibo...</h1><p>Refresca en unos segundos.</p>"


def payment_cancel():
    return "<h1>Pago Cancelado</h1><p>No se realizó ningún cargo. Puedes intentarlo de nuevo cuando quieras.</p>"






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
        

        transaction = PaymentTransaction.query.filter_by(externalReference=stripe_session_id).first()
        if transaction:
            process_successful_payment(transaction, session, app_name)

    # CASO 2: COBROS RECURRENTES AUTOMÁTICOS (MES 2, 3...)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice_data = event['data']['object']
  
        # Si es el pago de una suscripción
        subscription_id = (
                invoice_data.get('subscription') or 
                invoice_data.get('parent', {}).get('subscription_details', {}).get('subscription')
            )
            
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
                
                process_successful_payment(new_trans, invoice_data, app_name)

    return jsonify({"status": "success"}), 200

# Función auxiliar para evitar repetir código de factura y email
def process_successful_payment(transaction, stripe_obj, app_name):
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
        client_plan.sestadoplancliente = "ACTIVE"
        # Aquí sumas un mes a la fecha de vencimiento actual
        # client_plan.dfin = (client_plan.dfin or datetime.now()) + timedelta(days=30)
    
    db.session.commit()

    # 4. Enviar Email
    try:
        # En invoice.payment_succeeded el email está en customer_email
        email_to = stripe_obj.get('customer_email') or stripe_obj.get('customer_details', {}).get('email')
        name_to = stripe_obj.get('customer_name') or stripe_obj.get('customer_details', {}).get('name') or "Cliente"
        
        send_email_template(
            subject=f"Tu Factura {num_factura} - {app_name}",
            to=[email_to],
            path_template="emails/es/invoice_ready.html",
            name=name_to,
            invoice_num=num_factura,
            amount=float(transaction.amount),
            currency=transaction.currency,
            plan_name=client_plan.plan.code if client_plan else "Suscripción",
            app_name=app_name
        )
    except Exception as e:
        print(f"Error enviando email: {e}")