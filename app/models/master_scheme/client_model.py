from ...extensions import db
from datetime import date
import uuid


class Client(db.Model):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "master"}

    clientId = db.Column(
        "idcliente",
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        "scliente",
        db.String(200),
        nullable=False
    )

    contactName = db.Column(
        "scontacto",
        db.String(200),
        nullable=False
    )

    phoneTypeId = db.Column(
        "idtipotelefono",
        db.SmallInteger,
        nullable=False
    )

    contactPhone = db.Column(
        "stelcontacto",
        db.String(20),
        nullable=False
    )

    documentTypeId = db.Column(
        "idtipodocumento",
        db.SmallInteger,
        nullable=True
    )

    documentNumber = db.Column(
        "sdocumento",
        db.String(50),
        nullable=True
    )

    businessName = db.Column(
        "srazonsocial",
        db.String(250),
        nullable=False
    )

    billingCountryId = db.Column(
        "idpaisfacturacion",
        db.Integer,
        nullable=True
    )

    billingCityId = db.Column(
        "idciudadfacturacion",
        db.Integer,
        nullable=True
    )

    billingSectorId = db.Column(
        "idsectorfacturacion",
        db.Integer,
        nullable=True
    )

    billingAddress = db.Column(
        "sdireccionfacturacion",
        db.String(500),
        nullable=True
    )

    billingEmail = db.Column(
        "semailfacturacion",
        db.String(150),
        nullable=True
    )

    createdAt = db.Column(
        "dfechaalta",
        db.Date,
        default=date.today
    )

    serviceStartDate = db.Column(
        "dfechainicioservicio",
        db.Date,
        nullable=True
    )

    isActive = db.Column(
        "bactivo",
        db.Boolean,
        default=True
    )

    comment = db.Column(
        "scomentario",
        db.Text,
        nullable=True
    )

    uuid = db.Column(
        "uuidcliente",
        db.UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4
    )

    schemaName = db.Column(
        "sesquema",
        db.String(50),
        nullable=False
    )

    # --------------------------------------------------
    # Representación (útil para logs / debug)
    # --------------------------------------------------
    def __repr__(self):
        return f"<Client id={self.clientId} name={self.name}>"

    # --------------------------------------------------
    # Serialización para API / JSON
    # --------------------------------------------------
    def to_dict(self):
        return {
            "id": self.clientId,
            "name": self.name,
            "contact_name": self.contactName,
            "phone_type_id": self.phoneTypeId,
            "contact_phone": self.contactPhone,
            "document_type_id": self.documentTypeId,
            "document_number": self.documentNumber,
            "business_name": self.businessName,
            "billing_country_id": self.billingCountryId,
            "billing_city_id": self.billingCityId,
            "billing_sector_id": self.billingSectorId,
            "billing_address": self.billingAddress,
            "billing_email": self.billingEmail,
            "created_at": self.createdAt.isoformat() if self.createdAt else None,
            "service_start_date": self.serviceStartDate.isoformat() if self.serviceStartDate else None,
            "is_active": self.isActive,
            "comment": self.comment,
            "uuid": str(self.uuid),
            "schema": self.schemaName,
        }
