import stripe
import os
from dotenv import load_dotenv
from flask import request

class StripeProvider:
    def __init__(self):
        load_dotenv()
        
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    def create_checkout(self, amount, currency, order_id, client_email):
        """
        Crea una sesión de pago en Stripe y devuelve la URL.
        """
        try:
            # Stripe maneja montos en centavos (ej: 100.00 DOP = 10000)
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
                    },
                    'quantity': 1,
                }],
                mode='payment',
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