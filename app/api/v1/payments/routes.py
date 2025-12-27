
from flask import Blueprint
from app.api.v1.payments.controller import stripe_webhook, payment_success, payment_cancel


payment_bp = Blueprint('payments', __name__, url_prefix="/api/v1")

# ... (configuración de stripe.api_key)


payment_bp.route('/payments/webhook', methods=['POST'])(stripe_webhook)
# payment_bp.route('/request_payment/<int:plan_identity>', methods=['POST'])(request_payment)
payment_bp.route('/payments/success', methods=['GET'])(payment_success)
payment_bp.route('/payments/cancel', methods=['GET'])(payment_cancel)

