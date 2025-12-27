import stripe
import os
from dotenv import load_dotenv
from flask import request

class StripeProvider:
    def __init__(self):
        load_dotenv()
        
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    def create_checkout(self, amount, currency, order_id, client_email, plan_period="month", is_trial_plan=False, trial_days=14):
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
            
            # 3. Creación de la Sesión
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'product_data': {
                            'name': f"Orden #{order_id}",
                        },
                        'unit_amount': amount_in_cents,
                        'recurring': {
                            'interval': interval,
                            'interval_count': interval_count,
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                # Pasamos el diccionario que preparamos arriba
                subscription_data=sub_data, 
                client_reference_id=order_id,
                customer_email=client_email,
                success_url=f"{request.host_url}api/v1/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
                #cancel_url=f"{request.host_url}api/v1/payments/cancel",
                cancel_url=f"{request.host_url}api/v1/payments/cancel?order_id={order_id}"
            )
            
            return {
                "url": session.url,
                "external_id": session.id
            }
        except Exception as e:
            print(f"Error en Stripe: {str(e)}")
            return None