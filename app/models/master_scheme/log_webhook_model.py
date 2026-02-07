from app import db
from datetime import datetime

class LogWebhook(db.Model):
    __tablename__ = 'logs_webhooks'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idlog', db.Integer, primary_key=True, autoincrement=True)
    provider = db.Column('sproveedor', db.String(50), default='NEOPAGOS')
    content = db.Column('jcontenido', db.JSON, nullable=False)
    is_processed = db.Column('bprocesado', db.Boolean, default=False)
    created_at = db.Column('dfecha', db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "provider": self.provider,
            "content": self.content,
            "is_processed": self.is_processed,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
