from flask import  request, jsonify, render_template
from ....extensions import db

from flask_jwt_extended import jwt_required, get_jwt_identity
from app import track_activity, require_role

from app.services.master_scheme.user_client_service import get_user_by_client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.user_model import User
from app.utils.responses import error, success
from dotenv import load_dotenv
import os
import stripe
from werkzeug.security import check_password_hash
from app.utils.helpers import send_confirmation_account_email
from app.services.master_scheme.payment_service import (handle_checkout_session_completed, handle_invoice_paid,
                                                        handle_invoice_payment_failed,handle_subscription_deleted,handle_subscription_updated, handle_subscription_trial_will_end)




# @jwt_required()
# @track_activity
# @require_role(["SUPER_ADMIN", "SYS_ADMIN"])
# @audit_log(action="REQUEST_PAYMENT", resource_type="transacciones_pagos",description="request payment")
# def request_payment(plan_identity):
#    data = request_suscription(plan_identity=plan_identity)
#    return success(data=data)



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

    event_type = event['type']
    data_object = event['data']['object']

    # Se dispara al completar con éxito el formulario de pago inicial (Suscripción o Trial)
    if event_type == 'checkout.session.completed':
        print('checkout.session.completed')
        handle_checkout_session_completed(data_object, app_name)
            
    # Se dispara cuando un cobro recurrente falla (ej. tarjeta sin fondos o expirada)
    elif event_type == 'invoice.payment_failed':
        print('invoice.payment_failed')
        handle_invoice_payment_failed(data_object, app_name)
            
    # Se dispara cada vez que un pago se realiza con éxito (Renovaciones mensuales/anuales)
    elif event_type == 'invoice.paid':
        print('invoice.paid')
        handle_invoice_paid(data_object, app_name)

    # Se dispara al cambiar fechas de periodo, planes (Upgrade/Downgrade) o estado de la suscripción
    elif event_type == "customer.subscription.updated":
        print("customer.subscription.updated")
        handle_subscription_updated(data_object)
        
    # Se dispara cuando la suscripción termina definitivamente (Fin de ciclo o cancelación total)
    elif event_type == "customer.subscription.deleted":
        print("customer.subscription.deleted")
        handle_subscription_deleted(data_object)
    
    # Se dispara 3 días antes de que el periodo de prueba finalice y se convierta en pago real
    elif event_type == "customer.subscription.trial_will_end":
        print("customer.subscription.trial_will_end")
        handle_subscription_trial_will_end(data_object, app_name)
    
    return jsonify({"status": "success"}), 200

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


#@app.route('/api/v1/subscriptions/cancel', methods=['POST']
@jwt_required()
@track_activity
def cancel_subscription():
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    password = data.get('password')
    user_id = get_jwt_identity()  

    if not subscription_id or not password:
            return jsonify({"success": False, "msg": "Datos incompletos"}), 400
    

        
    try:

        
        client = Client.query.filter_by(stripe_subscription_id=subscription_id).first()
        if not client:
            return error(message="Invalid suscription")  
            
        user = User.query.get(user_id)
        if not user:
            return error(message="not user found")    
            
        def verificar_password(hash_stored: str, password: str) -> bool:
            """Verifica la contraseña comparando con el hash almacenado."""
            return check_password_hash(hash_stored, password)
        
        if not verificar_password(user.password, password):
            return error(message="Credenciales inválidas", status_code=401)
        
        relacion = UsuarioCliente.query.filter_by(client_uuid=client.uuid).first()
        if not relacion or relacion.user_id != user_id:
            return error(message="Este usuario no esta relacionado a ningun cliente")
        
        if not user.rol or  user.rol not in ("ADMIN", "OWNER"):
                    return jsonify({"success": False, "msg": "Nivel de privilegios insuficiente"}), 403
            
            
        
        # Cancelación inmediata
        deleted_subscription = stripe.Subscription.delete(subscription_id)
        
        #El cliente sigue teniendo acceso hasta que termine el mes que ya pagó.
        # stripe.Subscription.modify(
        #     subscription_id,
        #     cancel_at_period_end=True
        # )
        
        # Aquí deberías actualizar tu base de datos: 
        # cliente.status = 'inactive'
        
        return jsonify({
            "success": True, 
            "status": deleted_subscription.status,
            "msg": "Suscripción cancelada exitosamente"
        }), 200

    except stripe.error.StripeError as e:
        return jsonify({"success": False, "msg": str(e)}), 400
# def stripe_webhook_old():
#     load_dotenv()
#     payload = request.data
#     sig_header = request.headers.get('Stripe-Signature')
#     endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
#     app_name = os.getenv("APP_NAME")
    
   
#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


#     print(event['type'])
#     # CASO 1: PAGO INICIAL (CHECKOUT)
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         stripe_session_id = session.get('id')
        

        
#         # En Checkout, el monto total nos dice si es Trial
#         # amount_total es 0 si es un inicio de periodo de prueba
#         is_trial = (session.get('amount_total') == 0)
        

#         transaction = PaymentTransaction.query.filter_by(externalReference=stripe_session_id).first()
#         if transaction:
#             transaction.rawResponse = session
#             process_successful_payment(transaction, session, app_name, is_trial=is_trial)
            
            
#     elif event['type'] == 'invoice.payment_failed':
#         # IMPORTANTE: Aquí manejamos si la tarjeta falló en la renovación
#         invoice = event['data']['object']
#         customer_id = invoice['customer']

#             # 1. Obtener detalles del error de Stripe
#         # Accedemos al último intento de pago para saber por qué falló
#         payment_intent_id = invoice.get('payment_intent')
#         failure_msg = "Rechazo general por parte del banco"
        
#         if payment_intent_id:
#             pi = stripe.PaymentIntent.retrieve(payment_intent_id)
#             if pi.last_payment_error:
#                 failure_msg = pi.last_payment_error.message
        
#         # 2. Buscar al cliente en la DB
#         client = Client.query.filter_by(stripe_customer_id=customer_id).first()
#         #client = Client.query.filter_by(clientId=1).first()
#         if client:
#             # 3. Cambiar estado a PAST_DUE (Vencido)
#             plan = ClientPlan.query.filter_by(client_id=client.clientId, status='ACTIVE').first()
#             if plan:
#                 plan.status = 'PAST_DUE'
#                 db.session.commit()

#             # 4. Enviar el Email
#             # Nota: update_payment_url debería ser el enlace a tu panel de configuración de facturación
#             send_email_template(
#                 subject="Acción requerida: Error en el pago de tu suscripción",
#                 to=[client.billingEmail],
#                 path_template="emails/es/payment_failed.html",
#                 name=client.contactName,
#                 app_name=os.getenv("APP_NAME"),
#                 plan_name=plan.plan.name if plan else "Suscripción Akdmia",
#                 amount=invoice['amount_due'] / 100, # Convertir de centavos
#                 currency=invoice['currency'].upper(),
#                 failure_reason=failure_msg,
#                 update_payment_url=f"{request.host_url}billing/settings" #TODO: esto debe ser trabajado para actualizar metodos de pago desde stripe
#             )
            

#     elif event['type'] == 'invoice.paid':
#         # CASO 2: COBROS RECURRENTES AUTOMÁTICOS (MES 2, 3...)
#         #elif event['type'] == 'invoice.payment_succeeded':
    
#         invoice_data = event['data']['object']
  
#         # Si es el pago de una suscripción
#         subscription_id = (
#                 invoice_data.get('subscription') or 
#                 invoice_data.get('parent', {}).get('subscription_details', {}).get('subscription')
#             )
            
#         # En Invoice, amount_paid nos dice si este ciclo fue gratuito
#         is_trial = (invoice_data.get('amount_paid') == 0)
        
#         print(f"DEBUG: Subscription ID encontrado -> {subscription_id}")
        
#         stripe_paid_at = invoice_data.get('status_transitions', {}).get('paid_at') or invoice_data.get('created')
        
#         # Convertir el timestamp de Stripe a datetime con zona horaria UTC
#         payment_date_dt = datetime.fromtimestamp(stripe_paid_at, tz=timezone.utc)
        
        
#         # Si quieres guardar también el inicio y fin del periodo pagado
#         period_start = datetime.fromtimestamp(invoice_data['lines']['data'][0]['period']['start'], tz=timezone.utc)
#         period_end = datetime.fromtimestamp(invoice_data['lines']['data'][0]['period']['end'], tz=timezone.utc)

            
#         if subscription_id:
#             # Buscamos la transacción anterior para identificar al cliente/plan
#             # Buscamos en el JSON rawResponse de transacciones previas
#             prev_trans = PaymentTransaction.query.filter(
#                 PaymentTransaction.rawResponse['subscription'].astext == subscription_id
#             ).first()

#             if prev_trans:
#                 # Creamos una NUEVA transacción para el nuevo periodo
#                 new_trans = PaymentTransaction(
#                     clientPlanId=prev_trans.clientPlanId,
#                     clientId=prev_trans.clientId,
#                     internalReference=f"REC-{int(datetime.now().timestamp())}",
#                     externalReference=invoice_data.get('payment_intent'), # ID del cobro actual
#                     amount=invoice_data.get('amount_paid') / 100,
#                     currency=invoice_data.get('currency').upper(),
#                     status="APPROVED",
#                     paymentDate=payment_date_dt,
#                     rawResponse=invoice_data
#                 )
#                 db.session.add(new_trans)
#                 db.session.flush() # Para obtener el ID de la transacción
                
#                 process_successful_payment(new_trans, invoice_data, app_name, is_trial)

#     elif event['type'] == "customer.subscription.updated":
#         # customer.subscription.updated: Se dispara cuando el usuario decide cancelar (pero aún tiene días restantes) o cuando cambia de plan (Upgrade/Downgrade).
#         subscription = event['data']['object']
#         stripe_cus_id = subscription['customer'] # Obtenemos el cus_...

#         # 1. Buscamos al cliente primero
#         client = Client.query.filter_by(stripe_customer_id=stripe_cus_id).first()
#         #client = Client.query.filter_by(clientId=1).first()

#         if client:
#             # 2. Ahora buscamos el plan ACTIVO de ese cliente
#             # (O el que coincida con esta suscripción si guardas el sub_...)
#             client_plan = ClientPlan.query.filter_by(
#                 client_id=client.clientId, 
#                 status='ACTIVE' 
#             ).first()

#             if client_plan:
#                 # 3. ACTUALIZAR FECHA DE VENCIMIENTO (dfin)
#                 # Convertimos el timestamp de Stripe a fecha de Python
#                 new_end_date = datetime.fromtimestamp(subscription['current_period_end']).date()
#                 client_plan.end_date = new_end_date # Tu campo dfin

#                 # 4. Sincronizar estado
#                 stripe_status = subscription['status']
#                 if stripe_status == 'active':
#                     client_plan.status = 'ACTIVE'
#                 elif stripe_status in ['past_due', 'unpaid']:
#                     client_plan.status = 'PAST_DUE'

#                 db.session.commit()
#                 print(f"DEBUG: Fecha dfin actualizada a {new_end_date} para el cliente {client.businessName}")
        
        
        
#     elif event['type'] == "customer.subscription.deleted":
#         # customer.subscription.deleted: Este es el evento final. Se dispara cuando el acceso debe cortarse definitivamente. Aquí es donde cambias el estado a INACTIVE en tu base de datos.
#         subscription = event['data']['object']
#         stripe_cus_id = subscription['customer']
        
#         # 1. Buscamos al cliente por su nuevo nombre de columna
#         client = Client.query.filter_by(stripe_customer_id=stripe_cus_id).first()
        
#         if client:
#             # 2. Buscamos el plan que estaba activo o en mora (past_due)
#             # Es vital buscar ambos porque un plan borrado suele venir de una mora
#             client_plan = ClientPlan.query.filter_by(client_id=client.clientId).filter(
#                 ClientPlan.status.in_(['ACTIVE', 'PAST_DUE', 'TRIAL'])
#             ).first()

#             if client_plan:
#                 # 3. CAMBIAR ESTADO A INACTIVO / CANCELADO
#                 client_plan.status = 'CANCELED'
                
#                 # 4. Opcional: Limpiar la fecha de vencimiento o registrar la fecha real de baja
#                 client_plan.end_date = datetime.now().date() 
                
                
#                 from app.models.master_scheme.user_client_model import UsuarioCliente
#                 from app.services.master_scheme.session_service import close_all_session
                
#                 #Obtener IDs de usuarios vinculados a este cliente a través de la intermedia
#                 user_ids_subquery = db.session.query(UsuarioCliente.user_id).filter(
#                                         UsuarioCliente.client_uuid == client.uuid
#                                     ).subquery()
                
                
#                 #Inhabilitar usuarios en masa
#                 User.query.filter(User.userId.in_(user_ids_subquery)).update(
#                     {"isActive": False}, 
#                     synchronize_session=False
#                 )
        
#                 #Cerrar sesiones (Iteramos para limpiar cache/Redis si es necesario)
#                 users_to_close = User.query.filter(User.userId.in_(user_ids_subquery)).all()
#                 for u in users_to_close:
#                     close_all_session(user_id=u.userId, commit=False)
                
                

#                 db.session.commit()
#                 print(f"❌ ACCESO REVOCADO: La suscripción del cliente {client.businessName} ha finalizado.")

#                 # 5. Acción adicional: Notificar al equipo de ventas o al cliente
#                 send_goodbye_email(client.billingEmail, client.contactName, business_name=client.businessName)
        
    
#     elif event['type'] == "customer.subscription.trial_will_end":
#         # Stripe lo envía 3 días antes de que acabe el trial. Es perfecto para enviar un email de: "Tu prueba termina pronto, asegúrate de tener fondos en tu tarjeta".
#         #session = event['data']['object'];
#         print("customer.subscription.trial_will_end --- ")
    
#     return jsonify({"status": "success"}), 200

