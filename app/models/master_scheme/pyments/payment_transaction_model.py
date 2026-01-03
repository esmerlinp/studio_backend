
from ....extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone


class PaymentTransaction(db.Model):
    __tablename__ = 'transacciones_pagos'
    __table_args__ = {"schema": "master"}

    id = db.Column("idtransaccion", db.Integer, primary_key=True)
    clientPlanId = db.Column("idplancliente", db.Integer, db.ForeignKey('master.planesclientes.idplancliente'))
    clientId = db.Column("idcliente", db.Integer, nullable=False)

    # NUEVO: Tu ID de orden interna (ej: TEST-ORDER-1735165)
    internalReference = db.Column("sreferencia_interna", db.String(100), unique=True, nullable=False)
    
    # AJUSTADO: El ID que genera Stripe (cs_test_...)
    externalReference = db.Column("sreferencia_pasarela", db.String(255), unique=True, index=True)
    
    amount = db.Column("dmonto", db.Numeric(12, 2), nullable=False)
    currency = db.Column("smoneda", db.String(10), default="DOP")
    status = db.Column("sestado", db.String(20), default="PENDING")
    
    paymentDate = db.Column("dfechapago", db.DateTime(timezone=True))
    rawResponse = db.Column("jrespuesta_pasarela", JSONB) 
    
    # Corregido para evitar el aviso de desuso
    createdAt = db.Column("dfecha_registro", db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "clientPlanId": self.clientPlanId,
            "internalReference": self.internalReference,
            "externalReference": self.externalReference,
            "rawResponse": self.rawResponse,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status,
            "paymentDate": self.paymentDate.isoformat() if self.paymentDate else None
        }