from datetime import datetime
from ....extensions import db


class Invoice(db.Model):
    __tablename__ = "facturas"
    __table_args__ = {"schema": "master"}

    id = db.Column("idfactura", db.Integer, primary_key=True)
    transactionId = db.Column("idtransaccion", db.Integer, db.ForeignKey("master.transacciones_pagos.idtransaccion"))
    
    invoiceNumber = db.Column("snumfactura", db.String(50), unique=True) # Ej: FAC-2024-001
    issueDate = db.Column("dfechaemision", db.DateTime, default=datetime.utcnow)
    
    # Datos fiscales o legales (puedes expandir esto)
    totalAmount = db.Column("dtotal", db.Numeric(12, 2))
    
    def to_dict(self):
        return {
            "invoiceNumber": self.invoiceNumber,
            "issueDate": self.issueDate.isoformat(),
            "total": float(self.totalAmount)
        }