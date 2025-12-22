

from sqlalchemy import text
from ..extensions import db
import re

from datetime import date
from sqlalchemy.exc import IntegrityError
from app.models.master.client_model import Client
from app.models.client.log_model import AuditLog

def validate_schema_name(schema: str):
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", schema):
        raise ValueError("Invalid schema name")



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
) -> Client:
    """
    Crea un cliente en master.clientes y su esquema de base de datos
    """

    client = Client(
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
        db.session.add(client)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("Ya existe un cliente con los datos proporcionados") from e

    except Exception as e:
        db.session.rollback()
        raise e

    try:
        # 2️⃣ Crear esquema del cliente
        create_client_schema(schema_name)

    except Exception as e:
        # ⚠️ Si falla el schema, el cliente queda inconsistente
        # Puedes decidir:
        # - eliminar el cliente
        # - o marcarlo inactivo
        client.isActive = False
        db.session.commit()

        raise RuntimeError(
            f"Cliente creado pero falló la creación del esquema '{schema_name}'"
        ) from e

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

    