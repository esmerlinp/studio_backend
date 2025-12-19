from ..extensions import db
import datetime

class Notification(db.Model):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "master"}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)

    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # 👉 CONTEXTO
    resource_type = db.Column(db.String(50), nullable=True)   # employee
    resource_id = db.Column(db.Integer, nullable=True)        # 123
    action = db.Column(db.String(50), nullable=True)          # created
    target_url = db.Column(db.String(255), nullable=True)     # /employees/123

    read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "read": self.read,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "action": self.action,
            "target_url": self.target_url,
            "created_at": self.created_at.isoformat()
        }
