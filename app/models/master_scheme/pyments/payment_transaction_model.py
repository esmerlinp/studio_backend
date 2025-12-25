from datetime import datetime
from ....extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class PaymentTransaction(db.Model):
    __tablename__ = 'transacciones_pagos'
    __table_args__ = {"schema": "master"}

    id = db.Column("idtransaccion", db.Integer, primary_key=True)
    
    # Vinculamos al contrato de suscripción que ya tienes
    clientPlanId = db.Column("idplancliente", db.Integer, db.ForeignKey('master.planesclientes.idplancliente'))
    clientId = db.Column("idcliente", db.Integer, nullable=False) # Copia directa para reportes rápidos

    # Referencia de Neopagos (Se llena cuando inicias el pago o vía Webhook)
    externalReference = db.Column("sreferencia_pasarela", db.String(100), unique=True, index=True)
    
    amount = db.Column("dmonto", db.Numeric(12, 2), nullable=False)
    currency = db.Column("smoneda", db.String(10), default="DOP")
    
    # Estados: PENDING, APPROVED, REJECTED, VOIDED
    status = db.Column("sestado", db.String(20), default="PENDING")
    
    # Información del pago recibida de Neopagos
    paymentDate = db.Column("dfechapago", db.DateTime)
    rawResponse = db.Column("jrespuesta_pasarela", JSONB) # Auditoría total del JSON recibido

    createdAt = db.Column("dfecha_registro", db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "clientPlanId": self.clientPlanId,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status,
            "externalReference": self.externalReference,
            "paymentDate": self.paymentDate.isoformat() if self.paymentDate else None
        }