
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
    
def request_suscription3(plan_identity) -> dict:
    provider = get_current_provider()
    
    # 1. Obtener datos del plan del cliente
    plan_del_cliente = get_active_plan(id=plan_identity)
    if not plan_del_cliente:
        return {"status": "error", "message": "Plan no encontrado"}

    client_id = plan_del_cliente.client_id
    client = Client.query.get(client_id)

    # 2. Extraer datos de la lista de precios
    price_info = plan_del_cliente.price_list
    amount = float(price_info.price)
    currency = price_info.currency
    #billing_cycle = price_info.billing_cycle # 'mensual', 'anual', etc.
    billing_cycle = "mensual" # 'mensual', 'anual', etc.
    is_trial = price_info.is_trial
    trial_days = price_info.trial_days

    # --- MEJORA: Validar si ya existe una transacción PENDING reciente ---
    # Esto evita que si el usuario hace click dos veces rápido, se creen dos órdenes
    
    # 3. CREAR TRANSACCIÓN EN TU DB
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

    # 4. LLAMAR A STRIPE
    # Usamos billing_cycle dinámico en lugar de "mensual" fijo
    stripe_session = provider.create_checkout(
        amount=amount,
        currency=currency,
        order_id=order_id,
        client_email=client.billingEmail,
        plan_period=billing_cycle,  # <--- DINÁMICO
        is_trial_plan=is_trial, 
        trial_days=trial_days
    )

    if stripe_session:
        new_trans.externalReference = stripe_session['external_id']
        db.session.commit()
    
        return {
            "status": "success",
            "checkout_url": stripe_session['url'],
            "stripe_id": stripe_session['external_id']
        }

    # Si falla Stripe, cancelamos la transacción interna
    new_trans.status = "FAILED"
    db.session.commit()
    return {"status": "error", "message": "No se pudo contactar con el proveedor de pagos"}



def request_suscription_old(plan_identity) -> dict:
    # 1. Obtenemos el proveedor (Stripe según tu .env)
    provider = get_current_provider()
    plan_del_cliente = get_active_plan(id=plan_identity)

    client_id = plan_del_cliente.client_id
    client = get_client_by_id(clientId=client_id)

    amount = float(plan_del_cliente.price_list.price)
    billing_cycle = plan_del_cliente.price_list.billing_cycle
    
    
    #amount = 220.00
    currency =  plan_del_cliente.price_list.currency  #"DOP"
    is_trial =  plan_del_cliente.price_list.is_trial  #"DOP"
    trial_days =  plan_del_cliente.price_list.trial_days  #"DOP"

    # 3. CREAR TRANSACCIÓN EN TU DB (Estado inicial)
    # Generamos una referencia interna para Stripe
    order_id = f"ORDER-{int(datetime.now(timezone.utc).timestamp())}"
    
    new_trans = PaymentTransaction(
        clientPlanId=plan_identity,
        clientId=client_id,
        amount=amount,
        currency=currency,
        internalReference= order_id,
        status="PENDING"
    )
    db.session.add(new_trans)
    db.session.commit()

    # 4. LLAMAR A STRIPE
    # Pasamos el internal_ref para que Stripe nos lo devuelva en el webhook
    stripe_session = provider.create_checkout(
        amount=amount,
        currency=currency,
        order_id=order_id,
        client_email=client.billingEmail,
        plan_period="mensual",  
        is_trial_plan=is_trial, 
        trial_days=trial_days
    )

    if stripe_session:
        new_trans.externalReference = stripe_session['external_id'] # <--- El cs_test_...
        db.session.commit()
    
        data = {
            "status": "success",
            "checkout_url": stripe_session['url'],
            "stripe_id": stripe_session['external_id']
        }
        return data

    
    return {}
