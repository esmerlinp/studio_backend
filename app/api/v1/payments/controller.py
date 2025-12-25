from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.master_scheme.payment_service import PaymentService

from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.pyments.invoice_model import Invoice
from app.models.master_scheme.client_plans_model import ClientPlan
from flask import jsonify
import datetime
from app import db
import os
from dotenv import load_dotenv

import stripe

payment_service = PaymentService()


@jwt_required()
def initiate_payment(plan_id):
    client_id = get_jwt_identity()
    
    try:
        result = payment_service.create_checkout_session(
            client_plan_id=plan_id, 
            client_id=client_id
        )
        return jsonify({
            "success": True,
            "data": result,
            "message": "Link de pago generado exitosamente"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": str(e)
        }), 500
        
        
        



def stripe_webhook():
    load_dotenv()
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        # Validar que el aviso realmente viene de Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Si el pago fue exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Aquí usamos el order_id que guardamos antes
        order_id = session.get('client_reference_id')
        
        # 1. Buscar la transacción en tu DB y marcarla como APPROVED
        # 2. Generar la factura
        # 3. Activar el plan del cliente
        print(f"¡Pago exitoso para la orden {order_id}!")

    return jsonify({"status": "success"}), 200


def neopagos_webhook():
    data = request.get_json()
    
    # 1. Buscar la transacción pendiente
    # Neopagos suele enviar un ID de referencia que tú les diste al inicio
    ref_pasarela = data.get('id_transaccion') 
    transaction = PaymentTransaction.query.filter_by(externalReference=ref_pasarela).first()

    if not transaction:
        return jsonify({"msg": "Transacción no encontrada"}), 404

    # 2. Actualizar estado de la transacción
    nuevo_estado = data.get('status') # Supongamos 'APPROVED' o 'REJECTED'
    transaction.status = nuevo_estado
    transaction.rawResponse = data

    if nuevo_estado == 'APPROVED':
        transaction.paymentDate = datetime.utcnow()
        
        # 3. ACCIÓN LIGADA A TU TABLA: Actualizar el ClientPlan
        c_plan = ClientPlan.query.get(transaction.clientPlanId)
        if c_plan:
            c_plan.status = "ACTIVE"
            # Si el pago es una renovación, podrías extender c_plan.end_date aquí
            
        # 4. Generar Factura automáticamente
        nueva_factura = Invoice(
            transactionId=transaction.id,
            invoiceNumber=f"INV-{transaction.id}-{datetime.utcnow().year}",
            totalAmount=transaction.amount
        )
        db.session.add(nueva_factura)

    elif nuevo_estado == 'REJECTED':
        c_plan = ClientPlan.query.get(transaction.clientPlanId)
        if c_plan:
            c_plan.status = "SUSPENDED"

    db.session.commit()
    return jsonify({"status": "ok"}), 200
