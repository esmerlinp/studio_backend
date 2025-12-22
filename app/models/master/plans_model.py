from datetime import datetime
from ...extensions import db

# INSERT INTO plans (code, name, environment_type)
# VALUES
# ('STANDARD', 'Standard Plan', 'SHARED'),
# ('PREMIUM', 'Premium Plan', 'DEDICATED');

class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(50), nullable=False, unique=True)  # BASIC, STANDARD, PREMIUM
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    max_users = db.Column(db.Integer, nullable=True)
    max_storage_gb = db.Column(db.Integer, nullable=True)

    support_level = db.Column(db.String(50), nullable=True)       # Basic, Priority, 24/7
    environment_type = db.Column(db.String(30), nullable=True)    # SHARED, DEDICATED

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Plan {self.code}>"

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "max_users": self.max_users,
            "max_storage_gb": self.max_storage_gb,
            "support_level": self.support_level,
            "environment_type": self.environment_type,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
