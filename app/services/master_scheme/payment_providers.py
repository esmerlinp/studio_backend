import stripe
import os
from dotenv import load_dotenv
from flask import request
from app.models.master_scheme.client_model import Client
from ...extensions import db
class StripeProvider:
    def __init__(self):
        load_dotenv()
        
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        
        
    def create_checkout(self, client_id, client_email, amount, currency, order_id,  plan_period="month", is_trial_plan=False, trial_days=14):
        load_dotenv()
        base_url = request.host_url

        try:
            # 1. Configuración del Ciclo
            interval = "month"
            interval_count = 1
            
            if plan_period == 'trimestral':
                interval_count = 3
            elif plan_period == 'semestral':
                interval_count = 6
            elif plan_period == 'anual':
                interval = "year"
                interval_count = 1
            
            # 2. Preparar subscription_data SOLO si es un plan trial
            sub_data = {}
            if is_trial_plan:
                sub_data['trial_period_days'] = trial_days

            amount_in_cents = int(float(amount) * 100)
            
            client = Client.query.get(client_id)
            # Creamos el cliente en Stripe (si no lo hemos hecho antes)
            if not client.stripe_customer_id:
                stripe_customer = stripe.Customer.create(
                    email=client.billingEmail,
                    name=client.businessName,
                    metadata={'internal_client_id': client.clientId}
                )
                client.stripe_customer_id = stripe_customer.id
                db.session.commit()
            
            tax_rates = []
            if client.billingCountryId == 1:
                ITBIS_ID = os.getenv('STRIPE_ITBIS_TAX_RATE')
                tax_rates.append(ITBIS_ID)
            
            
            contract_summary = (
                f"Suscripción {plan_period}. Renovación automática. "
                "Cancelación disponible en cualquier momento desde el panel. "
                "Al pagar, aceptas nuestros términos: https://akdmia.com/terms"
            )
            
            # 3. Creación de la Sesión
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'product_data': {
                            'name': f"Orden #{order_id}",
                            'description': contract_summary, 
                            #'images': ['https://tu-sitio.com/plan-icon.png'],
                        },
                        'unit_amount': amount_in_cents,
                        'recurring': {
                            'interval': interval,
                            'interval_count': interval_count,
                        },
                    },
                    'quantity': 1,
                    'tax_rates': tax_rates, # <--- Aplica el impuesto a este ítem
                }],
                mode='subscription',
                # Pasamos el diccionario que preparamos arriba
                subscription_data=sub_data, 
                client_reference_id=order_id,
                customer=client.stripe_customer_id, # IMPORTANTE: Vinculamos la sesión al cliente
                #customer_email=client.billingEmail,
                success_url=f"{base_url}api/v1/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
                #cancel_url=f"{request.host_url}api/v1/payments/cancel",
                cancel_url=f"{base_url}api/v1/payments/cancel?order_id={order_id}"
            )
            
            return {
                "url": session.url,
                "external_id": session.id
            }
        except Exception as e:
            print(f"Error en Stripe: {str(e)}")
            return None