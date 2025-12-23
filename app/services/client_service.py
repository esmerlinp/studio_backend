

from sqlalchemy import text
from ..extensions import db
import re

from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from app.models.master.client_model import Client
from app.models.client.log_model import AuditLog
from sqlalchemy.exc import SQLAlchemyError
from app.services.client_plan_service import assign_plan_to_client, assign_plan_to_client_onboard
from app.services.plan_service import get_plans
from app.services.price_list_service import get_price_lists
from app.services.user_role_service import assign_role_to_user
from app.services.user_service import insert_user, insert_user_onboard
from app.services.user_client_service import assign_user_to_client, assign_user_to_client_onboard
from typing import Optional
from uuid import uuid4


def set_schema(schema_name: str):
    db.session.execute(
        text('SET search_path TO :schema, public'),
        {"schema": schema_name}
    )
    
def drop_schema(schema_name: str):
    """
    Elimina un esquema PostgreSQL de forma segura.
    """
    stmt = text(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
    db.session.execute(stmt)
    db.session.commit()
  
  

def schema_exists(schema_name: str) -> bool:
    """
    Verifica si un esquema existe en la base de datos PostgreSQL.
    """
    query = text("""
        SELECT EXISTS(
            SELECT 1 
            FROM information_schema.schemata 
            WHERE schema_name = :schema
        )
    """)
    result = db.session.execute(query, {"schema": schema_name}).scalar()
    return bool(result)
     
  

def onboard_client_service(client_data, admin_user_data, plan_id, price_list_id):

    schema_name = client_data["schema_name"]

    try:
        # 1️⃣ Crear schema (NO transaccional)
        if not schema_exists(schema_name):
            create_client_schema(schema_name)

        # 2️⃣ Transacción REAL solo para datos
        with db.session.begin():  # ← NO usar commit/rollback manual
            
            #Crear el cliente
            client = create_client(
                **client_data,
                commit=False
            )
            #asignarle un plan 
            assign_plan_to_client_onboard(
                client_id=client.clientId,
                plan_id=plan_id,
                price_list_id=price_list_id,
                start_date=date.today(),
            )
            
            #crear el usuario owner
            admin_user = insert_user_onboard(
                **admin_user_data,
                uuid=client.uuid,
                default_password=True,
            )
            #TODO: se debe cerar la tabla roles en el scheme master.
            
            # if schema_exists(client.schemaName):
            #   # 3. Cambiar al schema del cliente
            #   set_schema(client.schemaName)
            #   #Asigno el rol del usuario en el scheme del cliente
            #   assign_role_to_user(
            #       user_id=admin_user.userId,
            #       role_id=1,
            #       commit=False
            #   )

            #asignar el usuario al cliente 
            assign_user_to_client_onboard(
                user_id=admin_user.userId,
                client_uuid=client.uuid,
            )


        # ✅ Si llega aquí, todo se confirmó automáticamente
        return client

    except Exception as e:
        # 🔥 rollback automático del with
        # 🧨 borrar schema manualmente
        if schema_exists(schema_name):
            drop_schema(schema_name)

        raise e


def onboard_client_service_old(client_data, admin_user_data, plan_id, price_list_id) -> Optional[Client]:
    """
    Flujo de onboarding completo para un cliente:
    - Crear cliente
    - Asignar plan y price_list
    - Crear schema
    - Crear usuario admin
    - Asigna rol owner a usuario
    - Asociar usuario al cliente
    """
    try:
        # 3️⃣ Crear schema si no existe
        if not schema_exists(client_data["schema_name"]):
            create_client_schema(client_data["schema_name"])
        
        if schema_exists(client_data["schema_name"]):      
          with db.session.begin():  # 🔥 TRANSACCIÓN REAL
            # 1️⃣ Crear cliente
            client = create_client_onboard(
                name=client_data["name"],
                contact_name=client_data["contact_name"],
                phone_type_id=client_data["phone_type_id"],
                contact_phone=client_data["contact_phone"],
                document_type_id=client_data["document_type_id"],
                document_number=client_data["document_number"],
                business_name=client_data["business_name"],
                billing_country_id=client_data["billing_country_id"],
                billing_city_id=client_data["billing_city_id"],
                billing_sector_id=client_data["billing_sector_id"],
                billing_address=client_data["billing_address"],
                billing_email=client_data["billing_email"],
                service_start_date=client_data.get("service_start_date"),
                comment=client_data.get("comment"),
                schema_name=client_data["schema_name"],
                is_active=client_data.get("is_active", True)
            )

            # 2️⃣ Asignar plan y price list
            assign_plan_to_client(
                client_id=client.clientId,
                plan_id=plan_id,
                price_list_id=price_list_id,
                start_date=datetime.now().date(),
                commit=False
            )


            # 4️⃣ Crear usuario admin
            admin_user = insert_user(
                username=admin_user_data["username"],
                first_name=admin_user_data["first_name"],
                last_name=admin_user_data["last_name"],
                email=admin_user_data["email"],
                uuid=client.uuid,
                password=admin_user_data["password"],
                is_active=True,
                is_confirmed_user=True,
                must_change_password=True,
                commit=False
            )
            
            # Agregar el rol del usuario en la tabla de roles
            assign_role_to_user(admin_user.userId, 1, commit=False) #TODO: rol 1 administrador general falta tabla de roles en scheme master

            # 5️⃣ Asociar usuario al cliente
            assign_user_to_client(
                user_id=admin_user.userId,
                client_uuid=client.uuid,
                commit=False
            )
            
        

          return client
        else:
          return None
    except Exception as e:
        db.session.rollback()
        # Si el schema fue creado parcialmente, borrarlo
        if schema_exists(client_data["schema_name"]):
            drop_schema(schema_name=client_data['schema_name'])
        raise e
     
     



def validate_schema_name(schema: str):
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", schema):
        raise ValueError("Invalid schema name")




def create_client_onboard(
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
        serviceStartDate=service_start_date,
        comment=comment,
        isActive=is_active,
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
        serviceStartDate=service_start_date,
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

    # try:
    #     #asociar plan al cliente
    #     # 2️⃣ Crear esquema del cliente
    #     create_client_schema(schema_name)

    # except Exception as e:
    #     # ⚠️ Si falla el schema, el cliente queda inconsistente
    #     # Puedes decidir:
    #     # - eliminar el cliente
    #     # - o marcarlo inactivo
    #     client.isActive = False
    #     db.session.commit()

    #     raise RuntimeError(
    #         f"Cliente creado pero falló la creación del esquema '{schema_name}'"
    #     ) from e
    client = get_client_by_uuid(uuid)
    return client


def create_client_schema(new_schema: str, base_schema: str = "cliente"):
    sql = f"""
    CREATE SCHEMA IF NOT EXISTS {new_schema};

    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN 
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = '{base_schema}'
        LOOP
            EXECUTE format(
                'CREATE TABLE {new_schema}.%I (LIKE {base_schema}.%I INCLUDING ALL)',
                r.tablename,
                r.tablename
            );
        END LOOP;
    END $$;
    """
    try:
      db.session.execute(text(sql))
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e


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


def get_client_logs()-> list[AuditLog]:    
    logs = AuditLog.query.all()
    return logs
  
def get_client()-> list[Client]:    
    clients = Client.query.all()
    return clients
  
def get_client_by_id(client_id)-> Client:    
    clients = Client.query.filter_by(clientId = client_id)
    return clients
  
def get_client_by_uuid(uuid)-> Client:    
    client = Client.query.filter_by(uuid = uuid).first()
    return client

    