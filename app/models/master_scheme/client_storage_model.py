from datetime import datetime
from ...extensions import db


class ClientStorage(db.Model):
    __tablename__ = 'client_storage'
    __table_args__ = {"schema": "master"}

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('master.clients.id'))
    used_storage_mb = db.Column(db.BigInteger, default=0) # Almacenado en MB o Bytes
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)