import stripe
import os
from dotenv import load_dotenv
from flask import request

class StripeProvider:
    def __init__(self):
        load_dotenv()
        
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    def create_checkout(self, amount, currency, order_id, client_email, plan_period="month"):
        """
        Crea una sesión de pago en Stripe y devuelve la URL.
        trimestral, semestral, anual, trial
        """
        try:
            # Stripe maneja montos en centavos (ej: 100.00 DOP = 10000)

            # 1. Lógica de mapeo de tu plan a parámetros de Stripe
            interval = "month"
            #interval = "day"
            interval_count = 1
            
            if plan_period == 'trimestral':
                interval_count = 3
            elif plan_period == 'semestral':
                interval_count = 6
            elif plan_period == 'anual':
                interval = "year"
                interval_count = 1
            
        
            amount_in_cents = int(float(amount) * 100)
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
                            'interval_count': interval_count, # <--- AQUÍ defines el ciclo
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                client_reference_id=order_id, # Tu ID interno para reconocerlo luego
                customer_email=client_email,
                success_url=f"{request.host_url}/api/v1/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{request.host_url}/api/v1/payments/cancel",
            )
            
            return {
                "url": session.url,
                "external_id": session.id
            }
        except Exception as e:
            print(f"Error en Stripe: {str(e)}")
            return None