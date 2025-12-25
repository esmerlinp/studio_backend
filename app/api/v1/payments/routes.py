
from flask import Blueprint
from app.api.v1.payments.controller import  neopagos_webhook, initiate_payment, stripe_webhook

from datetime import datetime, timezone
from flask_jwt_extended import jwt_required

payment_bp = Blueprint('payments', __name__, url_prefix="/api/v1")


from flask import Blueprint, jsonify
from app.services.master_scheme.payment_factory import get_current_provider
from ....extensions import db
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
import os
from dotenv import load_dotenv



from flask import Blueprint, request, render_template, jsonify
import stripe

# ... (configuración de stripe.api_key)


def payment_success():
    # 1. Obtenemos el session_id de la URL
    load_dotenv()
        
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    session_id = request.args.get('session_id')
    
    try:
        # 2. (Opcional) Consultar Stripe para mostrar detalles reales
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.customer_details.email
        amount = session.amount_total / 100 # Convertir de centavos
        
        # Aquí podrías simplemente renderizar una página de "Gracias"
        return f"<h1>¡Pago Exitoso!</h1><p>Gracias {customer_email}, hemos recibido tu pago de {amount} {session.currency.upper()}.</p>"
    
    except Exception as e:
        return "El pago fue procesado, pero hubo un error al mostrar el recibo.", 400


def payment_cancel():
    return "<h1>Pago Cancelado</h1><p>No se realizó ningún cargo. Puedes intentarlo de nuevo cuando quieras.</p>"


@jwt_required()
def test_payment(plan_id):
    # 1. Obtenemos el proveedor (Stripe según tu .env)
    provider = get_current_provider()
    
    # 2. Simulamos datos (En un caso real vendrían de tu DB)
    client_id = 1
    amount = 500.00  # 500 pesos/dólares
    currency = "DOP"
    
    # 3. CREAR TRANSACCIÓN EN TU DB (Estado inicial)
    # Generamos una referencia interna para Stripe
    internal_ref = f"TEST-ORDER-{int(datetime.now(timezone.utc).timestamp())}"
    
    new_trans = PaymentTransaction(
        clientPlanId=plan_id,
        clientId=client_id,
        amount=amount,
        currency=currency,
        externalReference=internal_ref,
        status="PENDING"
    )
    db.session.add(new_trans)
    db.session.commit()

    # 4. LLAMAR A STRIPE
    # Pasamos el internal_ref para que Stripe nos lo devuelva en el webhook
    stripe_session = provider.create_checkout(
        amount=amount,
        currency=currency,
        order_id=internal_ref,
        client_email="test_user@example.com"
    )

    if stripe_session:
        return jsonify({
            "status": "success",
            "checkout_url": stripe_session['url'],
            "stripe_id": stripe_session['external_id']
        })
    
    return jsonify({"status": "error", "msg": "No se pudo crear la sesión"}), 500


payment_bp.route('/initiate/<int:plan_id>', methods=['POST'])(initiate_payment)
payment_bp.route('/webhooks/neopagos', methods=['POST'])(neopagos_webhook)
payment_bp.route('/webhooks/stripe', methods=['POST'])(stripe_webhook)
payment_bp.route('/test-stripe-payment/<int:plan_id>', methods=['POST'])(test_payment)
payment_bp.route('/payments/success', methods=['GET'])(payment_success)
payment_bp.route('/payments/cancel', methods=['GET'])(payment_cancel)


