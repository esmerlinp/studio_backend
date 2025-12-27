

from sqlalchemy import text
from ...extensions import db
import re
from sqlalchemy.exc import IntegrityError
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.user_model import User
from app.models.master_scheme.plans_model import Plan
from app.models.master_scheme.client_storage_model import ClientStorage
from app.models.master_scheme.client_plans_model import ClientPlan
from app.models.master_scheme.pyments.payment_transaction_model import PaymentTransaction
from app.models.client_scheme.log_model import AuditLog
from app.services.master_scheme.client_plan_service import assign_plan_to_client_onboard
from app.services.master_scheme.user_service import  insert_user_onboard
from app.services.master_scheme.user_client_service import  assign_user_to_client_onboard
from uuid import uuid4
from datetime import date
import uuid
from sqlalchemy import func

from typing import Optional, List
from app.services.master_scheme.payment_service import request_suscription
from app.utils.helpers import send_email_template
import os
from dotenv import load_dotenv

def set_schema(schema_name: str):
    db.session.execute(
        text('SET search_path TO :schema, public'),
        {"schema": schema_name}
    )
    
def onboard_client_service(client_data, admin_user_data, plan_data):
    load_dotenv()
    
    def deterministic_short_uuid(value, length=8):
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(value)).hex[:length]

    sname = deterministic_short_uuid(f"{admin_user_data['email']}_{client_data['business_name']}")
    schema_name = f"scheme_{sname}"
    email = admin_user_data["email"]

    try:
        # 1. Verificar si el Cliente ya existe (por email de facturación)
        client = Client.query.filter_by(billingEmail=email).first()
        
        if not client:
            contact_name = f"{admin_user_data['first_name']} {admin_user_data['last_name']}"
            client = create_client_onboard(
                contact_name=contact_name,
                contact_phone=client_data["contact_phone"],
                business_name=client_data["business_name"],
                billing_email=email,
                schema_name=schema_name
            )
            db.session.flush() # Obtenemos ID sin confirmar transacción completa
        
        # 2. Verificar si ya tiene un Plan
        client_plan = ClientPlan.query.filter_by(client_id=client.clientId).first()
        
        if not client_plan:
            client_plan = assign_plan_to_client_onboard(
                client_id=client.clientId,
                plan_id=plan_data["plan_id"], 
                price_list_id=plan_data["price_list_id"], 
                start_date=date.today(),
                status="PENDING_PAYMENT"
            )
            db.session.flush()

        # 3. Verificar si el Usuario ya existe
        admin_user = User.query.filter_by(email=email).first()
        
        if not admin_user:
            admin_user = insert_user_onboard(
                username=email,
                first_name=admin_user_data["first_name"],
                last_name=admin_user_data["last_name"],
                email=email,
                uuid=client.uuid,
                default_password=True,
            )
            db.session.flush()

            # 4. Asegurar la relación Usuario-Cliente
            # (Asumiendo que assign_user_to_client maneja si ya existe la relación)
            
            assign_user_to_client_onboard(
                user_id=admin_user.userId,
                client_uuid=client.uuid,
            )

        # 5. COMMIT de los datos base
        db.session.commit()

        # 6. Intentar generar la suscripción (Esto es lo que solía fallar)
        subscription_data = request_suscription(plan_identity=client_plan.id)
        
        if not subscription_data or subscription_data.get("status") != "success":
            # Aquí ya no hacemos rollback de los datos anteriores porque ya son válidos
            error_msg = subscription_data.get("message", "Error desconocido en Stripe")
            return {
                "status": "error",
                "message": f"Cuenta creada, pero hubo un error con Stripe: {error_msg}",
                "client_id": client.clientId,
                "retry_allowed": True # Informamos al front que puede reintentar solo el pago
            }

        checkout_url = subscription_data["checkout_url"]
        app_name = os.getenv("APP_NAME")

        # 7. Enviar email de respaldo
        try:
            send_email_template(
                subject=f"Completa tu registro en {app_name}",
                to=[email],
                path_template="emails/es/complete_subscription.html",
                name=admin_user_data["first_name"],
                plan_name=client_plan.plan.code,
                checkout_url=checkout_url,
                app_name=app_name
            )
        except Exception as email_err:
            print(f"Error no crítico enviando email: {email_err}")

        return {
            "status": "success",
            "checkout_url": checkout_url,
            "client_id": client.clientId
        }

    except Exception as e:
        db.session.rollback()
        print(f"Error fatal en onboard: {str(e)}")
        raise e
       
def validate_schema_name(schema: str):
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", schema):
        raise ValueError("Invalid schema name")

def create_client_onboard(
    *,
    contact_name: str| None = None,
    phone_type_id: int = 1,
    contact_phone: str,
    business_name: str,
    schema_name: str,
    billing_email: str | None = None,
) -> Client:
    """
    Crea un cliente en master.clientes y su esquema de base de datos
    """
    uuid = str(uuid4())
    new_client = Client(
        uuid=uuid,
        name=business_name,
        contactName=contact_name,
        phoneTypeId=phone_type_id,
        contactPhone=contact_phone,
        businessName=business_name,
        billingEmail=billing_email,
        serviceStartDate=date.today(),
        isActive=False,
        schemaName=schema_name,
    )
  

    validate_schema_name(schema=schema_name)
    # 1️⃣ Crear cliente en MASTER
    db.session.add(new_client)
    client = get_client_by_uuid(uuid)
    return client

def create_client(
    *,
    name: str,
    contact_name: str,
    phone_type_id: int,
    contact_phone: str,
    document_type_id: int,
    document_number: str,
    business_name: str,
    billing_country_id: int,
    billing_city_id: int,
    billing_sector_id: int,
    billing_address: str,
    schema_name: str,
    billing_email: str | None = None,
    service_start_date: date | None = None,
    comment: str | None = None,
    is_active: bool = True,
    commit: bool = True
) -> Client:
    """
    Crea un cliente en master.clientes y su esquema de base de datos
    """
    uuid = str(uuid4())
    new_client = Client(
        uuid=uuid,
        name=name,
        contactName=contact_name,
        phoneTypeId=phone_type_id,
        contactPhone=contact_phone,
        documentTypeId=document_type_id,
        documentNumber=document_number,
        businessName=business_name,
        billingCountryId=billing_country_id,
        billingCityId=billing_city_id,
        billingSectorId=billing_sector_id,
        billingAddress=billing_address,
        billingEmail=billing_email,
        serviceStartDate=date.today(),
        comment=comment,
        isActive=is_active,
        schemaName=schema_name,
    )
  

    try:
        validate_schema_name(schema=schema_name)
        # 1️⃣ Crear cliente en MASTER
        db.session.add(new_client)
        if commit:
          db.session.commit()
        else:
          db.session.flush()

    except IntegrityError as e:
        if commit:
          db.session.rollback()
        raise ValueError("Ya existe un cliente con los datos proporcionados") from e

    except Exception as e:
        if commit:
          db.session.rollback()
        raise e


    client = get_client_by_uuid(uuid)
    return client

def get_client_preferences():
  
  client_preferences = [
    {
      "id": 1,
      "cliente_id": 10,
      "idle_timeout_minutes": 30,
      "password_expiration_days": 90,
      "max_login_attempts": 5,
      "refresh_token_expiration_days": 7,
      "enforce_2fa": False,

      "timezone": "America/Santo_Domingo",
      "language": "es",
      "date_format": "DD/MM/YYYY",
      "company_logo_url": "https://example.com/logo_cliente10.png",

      "modules_enabled": {
        "payroll": True,
        "recruitment": True,
        "attendance": False
      },

      "created_at": "2025-01-10T12:30:00",
      "updated_at": "2025-01-15T08:00:00"
    },
    {
      "id": 2,
      "cliente_id": 20,
      "idle_timeout_minutes": 45,
      "password_expiration_days": 60,
      "max_login_attempts": 3,
      "refresh_token_expiration_days": 10,
      "enforce_2fa": True,

      "timezone": "America/Mexico_City",
      "language": "en",
      "date_format": "MM-DD-YYYY",
      "company_logo_url": "https://example.com/logo_cliente20.png",

      "modules_enabled": {
        "payroll": True,
        "recruitment": True,
        "attendance": True,
        "reporting": True
      },

      "created_at": "2025-02-02T14:20:00",
      "updated_at": "2025-02-08T09:50:00"
    }
  ]
    #user_id = get_jwt_identity()  # devuelve lo que enviaste como identity

    # user = user_model.get_user_by_id(user_id=int(user_id))
    # is_admin = db.fetch_one("select idrol from usuariosroles where idusuario=%s and idrol=1", (int(user_id),))
    # if not is_admin:
    #     return jsonify({"msg": "Acceso no autorizado"}), 403
    
    
  return {"user_id": 1, "preferences": []}

def get_client_logs()-> List[AuditLog]:    
    logs = AuditLog.query.all()
    return logs
  
def get_clients() -> List[Client]:    
    """
    Obtiene todos los clientes. 
    Usamos 'joinedload' si vas a necesitar datos de tablas relacionadas (como sus planes).
    """
    # .options(joinedload(Client.plan)) <-- Solo si tienes relaciones
    return Client.query.order_by(Client.clientId.desc()).all()
  
def get_client_by_id(clientId)-> Optional[Client]:    
    client = Client.query.get(clientId)
    return client
  
def get_client_by_uuid(uuid)-> Client:    
    client = Client.query.filter_by(uuid = uuid).first()
    return client

def get_client_payment_orders(client_id)-> List[PaymentTransaction]:    
    orders = PaymentTransaction.query.filter_by(clientId =client_id).all()
    return orders

def get_client_payment_orders_by_status(client_id, status_order)-> List[PaymentTransaction]:    
    orders = PaymentTransaction.query.filter_by(clientId =client_id, status=status_order).all()
    return orders

def has_available_storage(client_id: int, new_file_size_mb: float) -> tuple[bool, Optional[str]]:
    """
    Verifica si el cliente tiene espacio suficiente en su plan contratado.
    Retorna (True, None) si hay espacio, o (False, mensaje_error) si no.
    """
    
    # 1. Obtener la configuración del cliente y su plan (Join optimizado)
    # Buscamos el límite en GB desde la tabla de Planes vinculada al Cliente
    client_data = db.session.query(ClientPlan, Plan)\
        .join(Plan, ClientPlan.plan_id == Plan.id)\
        .filter(ClientPlan.client_id == client_id).first()

    if not client_data:
        return False, "Cliente o plan no encontrado."

    client, plan = client_data
    limit_mb = plan.max_storage_gb * 1024 # Convertimos GB a MB para comparar

    # 2. Obtener el consumo actual de la tabla de métricas
    storage_record = ClientStorage.query.filter_by(client_id=client_id).first()
    
    # Si no existe registro aún (cliente nuevo), su consumo es 0
    current_usage_mb = storage_record.used_storage_mb if storage_record else 0

    # 3. Lógica de validación
    projected_usage = current_usage_mb + new_file_size_mb

    if projected_usage > limit_mb:
        msg = f"Límite excedido. Tu plan permite {plan.storage_limit_gb}GB. Uso actual: {round(current_usage_mb/1024, 2)}GB."
        return False, msg

    return True, None

def storage_info(client_id) -> ClientStorage:
    storage = ClientStorage.query.filter_by(client_id=client_id).first()
    return storage
    
def update_client_storage_usage(client_id: int, size_mb: float, operation: str = "add"):
    """
    Actualiza el contador de almacenamiento consumido por un cliente.
    
    :param client_id: ID del cliente (tenant)
    :param size_mb: Tamaño a sumar o restar en MB
    :param operation: "add" para sumar, "subtract" para restar
    """
    try:
        # 1. Buscar el registro de almacenamiento del cliente
        storage_record = ClientStorage.query.filter_by(client_id=client_id).first()

        # 2. Si no existe (primer archivo del cliente), lo creamos
        if not storage_record:
            if operation == "subtract":
                return # No se puede restar de algo que no existe
            
            storage_record = ClientStorage(
                client_id=client_id, 
                used_storage_mb=0
            )
            db.session.add(storage_record)

        # 3. Aplicar la operación
        if operation == "add":
            storage_record.used_storage_mb += size_mb
        elif operation == "subtract":
            # Aseguramos que el contador no baje de cero
            storage_record.used_storage_mb = max(0, storage_record.used_storage_mb - size_mb)

        storage_record.last_updated = func.now()

        # 4. Confirmar cambios
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando cuota de almacenamiento: {str(e)}")
        return False