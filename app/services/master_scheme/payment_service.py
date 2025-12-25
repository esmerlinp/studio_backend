import requests
from flask import current_app
from app import db
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.master_scheme.client_plans_model import ClientPlan
from datetime import datetime
import os
from dotenv import load_dotenv

    
class PaymentService:
    def __init__(self):
        load_dotenv()
        # Estos valores deben estar en tu archivo .env o config.py
        self.api_key = os.getenv("NEOPAGOS_API_KEY")
        self.base_url = "https://api.neopagos.com/v1" # Ajustar según documentación oficial

    def create_checkout_session(self, client_plan_id, client_id):
        """
        Inicia el proceso de pago: Crea registro en DB y solicita link a Neopagos.
        """
        try:
            # 1. Obtener los datos del plan para saber cuánto cobrar
            client_plan = ClientPlan.query.get(client_plan_id)
            if not client_plan:
                raise Exception("Plan de cliente no encontrado")

            amount = float(client_plan.price_list.price)
            currency = client_plan.price_list.currency

            # 2. Crear la transacción en estado PENDING en nuestra base de datos
            # Generamos una referencia interna única antes de llamar a la pasarela
            internal_ref = f"PAY-{client_id}-{int(datetime.utcnow().timestamp())}"
            
            transaction = PaymentTransaction(
                clientPlanId=client_plan_id,
                clientId=client_id,
                amount=amount,
                currency=currency,
                externalReference=internal_ref, # Referencia temporal
                status="PENDING"
            )
            db.session.add(transaction)
            db.session.commit()

            # 3. Llamada a la API de Neopagos para obtener el link de pago
            # Nota: El payload depende de la documentación específica de Neopagos
            payload = {
                "amount": amount,
                "currency": currency,
                "description": f"Pago de suscripción - {client_plan.plan.name}",
                "order_id": internal_ref,
                "success_url": "https://tuapp.com/payment-success",
                "cancel_url": "https://tuapp.com/payment-failed",
                "notification_url": "https://tuapi.com/webhooks/neopagos" # Tu webhook
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(f"{self.base_url}/checkout", json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                # 4. Actualizamos la referencia externa con la que nos da la pasarela si es necesario
                # y guardamos el link de pago para retornar al frontend
                payment_url = response_data.get('checkout_url')
                transaction.externalReference = response_data.get('id_transaccion_pasarela', internal_ref)
                db.session.commit()

                return {
                    "payment_url": payment_url,
                    "transaction_id": transaction.id
                }
            else:
                transaction.status = "FAILED"
                db.session.commit()
                raise Exception(f"Error con Neopagos: {response_data.get('message')}")

        except Exception as e:
            db.session.rollback()
            raise e