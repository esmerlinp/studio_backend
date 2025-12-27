
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.services.master_scheme.client_plan_service import get_active_plan, get_active_pending
from app.models.master_scheme.client_model import Client
from datetime import datetime, timezone
from app.services.master_scheme.payment_factory import get_current_provider
from ...extensions import db




def request_suscription(plan_identity) -> dict:
    provider = get_current_provider()
    
    try:
        # 1. Obtener datos del plan
        plan_del_cliente = get_active_pending(id=plan_identity)
        if not plan_del_cliente:
            return {"status": "error", "message": "Plan no encontrado"}

        client_id = plan_del_cliente.client_id
        # Cambiamos la forma de consultar para asegurar que esté en la sesión actual
        client = db.session.get(Client, client_id) 

        # 2. Datos de precios
        price_info = plan_del_cliente.price_list
        amount = float(price_info.price)
        currency = price_info.currency
        billing_cycle = "mensual" 
        is_trial = price_info.is_trial
        trial_days = price_info.trial_days

        # 3. Crear transacción PENDING
        order_id = f"ORDER-{int(datetime.now(timezone.utc).timestamp())}"
        
        new_trans = PaymentTransaction(
            clientPlanId=plan_identity,
            clientId=client_id,
            amount=amount,
            currency=currency,
            internalReference=order_id,
            status="PENDING",
        )
        db.session.add(new_trans)
        db.session.commit()

        # 4. LLAMAR A STRIPE con bloque Try específico
        try:
            stripe_session = provider.create_checkout(
                amount=amount,
                currency=currency,
                order_id=order_id,
                client_email=client.billingEmail,
                plan_period=billing_cycle,
                is_trial_plan=is_trial, 
                trial_days=trial_days
            )
            
            if stripe_session and 'url' in stripe_session:
                new_trans.externalReference = stripe_session['external_id']
                db.session.commit()
                return {
                    "status": "success",
                    "checkout_url": stripe_session['url'],
                    "stripe_id": stripe_session['external_id']
                }
            else:
                raise Exception("Stripe no devolvió una URL válida")

        except Exception as stripe_err:
            # Si falla Stripe, marcamos la transacción como fallida
            new_trans.status = "FAILED"
            db.session.commit()
            print(f"❌ ERROR EN STRIPE PROVIDER: {str(stripe_err)}")
            return {"status": "error", "message": f"Error en Stripe: {str(stripe_err)}"}

    except Exception as e:
        db.session.rollback()
        print(f"❌ ERROR GENERAL EN REQUEST_SUSCRIPTION: {str(e)}")
        return {"status": "error", "message": str(e)}
    
