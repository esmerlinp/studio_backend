from flask import  request, jsonify, render_template
from app import db, require_role

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.master_scheme.user_client_service import get_user_by_client
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.user_model import User
from app.utils.responses import error, success
from app.utils.types import Roles as r
from dotenv import load_dotenv
import os, stripe
from werkzeug.security import check_password_hash
from app.utils.helpers import send_confirmation_account_email
from app.services.master_scheme.payment_service import (handle_checkout_session_completed, handle_invoice_created, handle_invoice_paid,
                                                        handle_invoice_payment_failed,handle_subscription_deleted,handle_subscription_updated, handle_subscription_trial_will_end)


from app.utils import i18n  # Importar el módulo de idiomas

def verificar_password(hash_stored: str, password: str) -> bool:
    """Verifica la contraseña comparando con el hash almacenado."""
    return check_password_hash(hash_stored, password)


def stripe_webhook():
    load_dotenv()
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    app_name = os.getenv("APP_NAME")

    # 1. Construir el evento
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # 2. VERIFICACIÓN DE IDEMPOTENCIA
    # Evita procesar el mismo evento dos veces si Stripe reintenta el envío
    event_id = event.get('id')
    if StripeEventLog.query.filter_by(stripe_event_id=event_id).first():
        print(f"Evento {event_id} ya procesado. Ignorando.")
        return jsonify({"status": "already_processed"}), 200

    # Registrar el evento para futuras verificaciones
    new_event_log = StripeEventLog(stripe_event_id=event_id, event_type=event['type'])
    db.session.add(new_event_log)
    db.session.commit()

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
        
    elif event_type == 'invoice.created':
        print('invoice.created')
        handle_invoice_created(data_object, app_name)

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
    lang = i18n.get_locale()
  
    # if not session_id:
    #     return redirect(url_for('home')) # O a tu página de precios

    # Intentamos buscar la transacción
    transaction = PaymentTransaction.query.filter_by(externalReference=session_id).first()
    
    # Si la transacción existe pero aún está "PENDING", es que el webhook no ha llegado.
    # En lugar de fallar, mostramos la vista de "Procesando" que haga un refresh automático.
    if not transaction or transaction.status == "PENDING":
        
        return render_template(f"{lang}/processing_payment.html", 
                               app_name=app_name, 
                               session_id=session_id)

    if transaction.status == "APPROVED":
        
        client = Client.query.get(transaction.clientId)
        client_plan = ClientPlan.query.filter_by(client_id=client.clientId)
        user = get_user_by_client(client.uuid)
        
        # 2. ENVIAR EMAIL (Solo si el usuario está inactivo o no ha seteado clave)
        # Esto evita que se re-envíe si el usuario refresca la página de éxito
        if user:
            send_confirmation_account_email(user.user.userId, client.contactName, user.user.email)
        
        invoice = Invoice.query.filter_by(transactionId=transaction.id).first()
        is_trial = (transaction.amount == 0)
        
        # Obtenemos el nombre del plan desde la relación si la tienes
        plan_name = "client_plan.plan.name"
        # if transaction.clientPlan:
        #     plan_name = transaction.clientPlan.plan.name

        # Usamos la nueva vista estética que diseñamos
        return render_template(
            f"{lang}/receipt_view.html", # Tu nueva plantilla estilo Stripe
            transaction=transaction,
            invoice=invoice,
            app_name=app_name,
            is_trial=is_trial,
            plan_name=plan_name,
            user_email=user.user.email # Pasamos el email para mostrarlo en el texto
        )
        
    return render_template(f"{lang}/error_payment.html", app_name=app_name)

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

@jwt_required()
def restore_canceled_subscription():
    try:
        # 1. Obtener al cliente y el ID del nuevo plan/precio
        load_dotenv()
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

        user_id = get_jwt_identity()
        relacion= UsuarioCliente.query.filter_by(user_id=user_id).first()
        client = Client.query.filter_by(uuid=relacion.client_uuid).first()        
        data = request.get_json()    
        price_id = data.get('price_id', None) #New price 
        new_pm_id = data.get('paymentMethodId') # ID de la nueva tarjeta si existe
        #client_id = data.get('clientId') 
        
        #client = Client.query.get(client_id)

        if not client.stripe_customer_id:
            return jsonify({"success": False, "msg": i18n._("error.payment.no_stripe_profile")}), 400
            
        
        
        if new_pm_id:
            # 1. Asociar nueva tarjeta al cliente
            stripe.PaymentMethod.attach(new_pm_id, customer=client.stripe_customer_id)
            # 2. Ponerla como predeterminada para facturas
            stripe.Customer.modify(
                client.stripe_customer_id,
                invoice_settings={"default_payment_method": new_pm_id}
            )
        
        if not price_id:
            # Opción A: Buscar el precio que el cliente tenía antes de cancelar
            plan_cliente = ClientPlan.query.filter_by(client_id=client.clientId).first()

            if plan_cliente.stripe_price_id:
                price_id = plan_cliente.stripe_price_id
                
            else:
                ultima_transaccion = PaymentTransaction.query.filter_by(
                    clientId=client.clientId, 
                    status="APPROVED"
                ).order_by(PaymentTransaction.id.desc()).first()

                subscription_id = ultima_transaccion.rawResponse.get('subscription')
                
                if subscription_id:
                    # 2. Le pedimos a Stripe los detalles de esa suscripción
                    old_sub = stripe.Subscription.retrieve(subscription_id)
                    
                    # 3. Extraemos el precio del primer item
                    price_id = old_sub['items']['data'][0]['price']['id']
                    print(f"Price ID recuperado de Stripe: {price_id}")
                    
    
            # Extraemos el price_id de la respuesta de Stripe que guardamos en JSON
            # if ultima_transaccion:
            #     price_id = ultima_transaccion.rawResponse.get('items', {}).get('data', [{}])[0].get('price', {}).get('id') # El ID del precio en Stripe (ej: price_123...)

        
        # 2. Crear una nueva suscripción en Stripe
        # Al crearla para un customer ya existente, usará su tarjeta predeterminada
        
        #Para que Stripe sepa cuánto cobrar de impuestos, el objeto Customer debe tener una dirección válida (especialmente el país y el código postal)
        # Actualizar dirección antes de cobrar impuestos

        tax_rates = []
        if client.billingCountryId == 1:
            ITBIS_ID = os.getenv('STRIPE_ITBIS_TAX_RATE')
            tax_rates.append(ITBIS_ID)
    
        new_subscription = stripe.Subscription.create(
            customer=client.stripe_customer_id,
            items=[{"price": price_id}],
            payment_behavior='default_incomplete', # Permite manejar fallos de pago
            default_tax_rates=tax_rates, # <--- Aplica el 18% desde el inicio
            expand=['latest_invoice.payment_intent'],
        )
        
        
        latest_invoice = new_subscription.latest_invoice
        # En la nueva API, el intent se recupera del objeto expandido
        payment_intent = getattr(latest_invoice, 'payment_intent', None)
        if payment_intent:
            # 1. Si el pago requiere autenticación (SCA / 3D Secure)
            if payment_intent.status == 'requires_action':
                # IMPORTANTE: No actives al cliente aún, el pago no es exitoso
                client.stripe_subscription_id = new_subscription.id
                db.session.commit()
                
                return jsonify({
                    "status": "requires_action",
                    "client_secret": payment_intent.client_secret,
                    "subscription_id": new_subscription.id,
                    "msg": i18n._("error.payment.auth_required")
                }), 200
            
            
            # CASO 2: Pago Exitoso (Succeeded) o ya Activo
            # Con la tarjeta 4242, el payment_intent suele quedar en 'succeeded' inmediatamente
            if payment_intent.status == 'succeeded':
                client.stripe_subscription_id = new_subscription.id
                client.isActive = True 
                db.session.commit()
                return jsonify({
                    "success": True, 
                    "status": "active",
                    "msg": i18n._("success.payment.restored"),
                    "subscription_id": new_subscription.id
                })
                
                
            # CASO 3: Fallo Real (Requires Payment Method)
            if payment_intent.status == 'requires_payment_method':
                payment_url = latest_invoice.hosted_invoice_url
                return jsonify({
                    "success": False,
                    "status": "payment_failed", # <--- Agrega este status para que tu JS lo capture
                    "msg": i18n._("error.payment.failed_retry"),
                    "url_actualizacion": payment_url
                }), 402
            

            # CASO DE RESPALDO: Si por alguna razón no hay intent pero la sub está activa
            if new_subscription.status == 'active':
                client.stripe_subscription_id = new_subscription.id
                client.isActive = True
                db.session.commit()
                return jsonify({"success": True, "status": "active", "msg": i18n._("success.payment.active")})

            # Si llega aquí, es un estado desconocido
            return jsonify({"success": False, "msg": i18n._("error.payment.unknown_status")}), 400

        # 2. CASO ESPECÍFICO TEST CLOCK / FACTURA ABIERTA
        # Si la factura está abierta y no hubo intento fallido, consideramos que el proceso inició bien
        if latest_invoice.status == 'open' or latest_invoice.status == 'draft':
            client.stripe_subscription_id = new_subscription.id
            # Nota: Con Test Clock, quizás no quieras poner isActive=True hasta que el webhook confirme el pago,
            # pero para desbloquear tus pruebas, lo activamos:
            client.isActive = True 
            db.session.commit()
            return jsonify({
                "success": True,
                "status": "pending_test_clock",
                "msg": i18n._("success.payment.pending_test_clock")
            })

        # 3. Si la factura falló
        if new_subscription.status == 'incomplete':
             return jsonify({
                "success": False,
                "msg": i18n._("error.payment.initial_failed"),
                "url_actualizacion": latest_invoice.hosted_invoice_url
            }), 402
             
    except stripe.error.StripeError as e:
        print(e)
        db.session.rollback()
        return jsonify({"success": False, "msg": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"success": False, "msg": i18n._("error.payment.generic_process")}), 500
    
      


def show_restore_view():
    load_dotenv()
    user_id = get_jwt_identity()
    relacion = UsuarioCliente.query.filter_by(user_id=user_id).first()
    
    if not relacion:
         return render_template("errors/404.html"), 404
         
    client = Client.query.filter_by(uuid=relacion.client_uuid).first()
    
    if not client:
        return render_template("errors/404.html"), 404
    
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    # Obtenemos el cliente de Stripe para ver su tarjeta predeterminada
    stripe_customer = stripe.Customer.retrieve(
        client.stripe_customer_id,
        expand=['invoice_settings.default_payment_method']
    )
    
    payment_method = stripe_customer.invoice_settings.default_payment_method
    print("payment_method, ", stripe_customer.invoice_settings)
    
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

@jwt_required()
def cancel_subscription():
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    password = data.get('password')
    user_id = get_jwt_identity()  
    
    load_dotenv()
        
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        

    if not subscription_id or not password:
        return jsonify({"success": False, "msg": i18n._("error.auth.incomplete_data")}), 400
    
    
    try:
        
        client = Client.query.filter_by(stripe_subscription_id=subscription_id).first()

        if not client:
            return error(message=i18n._("error.payment.invalid_subscription"))  
            
        user = User.query.get(user_id)
        if not user:
            return error(message=i18n._("error.auth.invalid_credentials"), status_code=401)    
            

        if not verificar_password(user.password, password):
            return error(message=i18n._("error.auth.invalid_credentials"), status_code=401)    
        
        
        relacion = UsuarioCliente.query.filter_by(client_uuid=client.uuid).first()

        
        # 1. Validar existencia primero
        if relacion is None:
            return error(message="La relación no existe")

        # 2. Validar pertenencia con casting de tipo para evitar el error de str vs int
        if str(relacion.user_id) != str(user_id):
            return error(message="Este usuario no está relacionado a la suscripción")
        
        
        if not user.rol or  user.rol not in (r.ADMIN, r.OWNER):
            return jsonify({"success": False, "msg": i18n._("error.auth.insufficient_permissions")}), 403
            
            
        
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
            "msg": i18n._("success.payment.cancelled")
        }), 200

    except stripe.error.StripeError as e:
        return jsonify({"success": False, "msg": str(e)}), 400

@jwt_required()
@require_role([r.ROOT, r.SYS_ADMIN, r.OWNER, r.AUDITOR])
def get_payment_detail(payment_id):
    transaction = PaymentTransaction.query.get(payment_id)
    if not transaction:
        return error(i18n._('error.payment.not_found'), 404)
        
    return success(data=transaction.to_dict())
