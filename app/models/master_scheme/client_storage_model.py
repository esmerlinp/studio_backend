from datetime import datetime
from ...extensions import db


class ClientStorage(db.Model):
    __tablename__ = 'cuotasalmacenamiento'
    __table_args__ = {"schema": "master"}

    id = db.Column("idcuotaalmacenamiento", db.Integer, primary_key=True)
    client_id = db.Column("idcliente", db.Integer, db.ForeignKey('master.clientes.idcliente'))
    #used_storage_mb = db.Column("iespusadomb", db.BigInteger, default=0) # Almacenado en MB o Bytes
    used_storage_mb = db.Column("iespusadomb", db.Float, default=0.0)
    last_updated = db.Column("dfechaactualizacion", db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "used_storage_mb": self.used_storage_mb,
            "last_updated": self.last_updated
        }