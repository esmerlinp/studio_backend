
from flask import Blueprint
from app.api.v1.master.payments.controller import (
    stripe_webhook, payment_success, payment_cancel, 
    cancel_subscription, restore_canceled_subscription, show_restore_view,
    get_payment_detail)


payment_bp = Blueprint('payments', __name__, url_prefix="/api/v1/master")
billing_bp = Blueprint('billing', __name__, url_prefix="/api/v1/master")

# ... (configuración de stripe.api_key)


payment_bp.route('/payments/webhook', methods=['POST'])(stripe_webhook)
# payment_bp.route('/request_payment/<int:plan_identity>', methods=['POST'])(request_payment)
payment_bp.route('/payments/success', methods=['GET'])(payment_success)
payment_bp.route('/payments/cancel', methods=['GET'])(payment_cancel)
payment_bp.post('/subscriptions/cancel')(cancel_subscription)
payment_bp.post('/subscriptions/restore')(restore_canceled_subscription)
payment_bp.get('/payments/<int:payment_id>')(get_payment_detail)

billing_bp.route('/billing/restore-2')(show_restore_view)