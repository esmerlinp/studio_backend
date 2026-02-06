from datetime import datetime
from ...extensions import db
from app.utils.helpers import format_datetime_user

# INSERT INTO plans (code, name, environment_type)
# VALUES
# ('STANDARD', 'Standard Plan', 'SHARED'),
# ('PREMIUM', 'Premium Plan', 'DEDICATED');

class Plan(db.Model):
    __tablename__ = "planes"
    __table_args__ = {"schema": "master"}


    id = db.Column("idplan", db.Integer, primary_key=True)

    code = db.Column("scodigoplan", db.String(50), nullable=False, unique=True)  # BASIC, STANDARD, PREMIUM
    name = db.Column("snombreplan", db.String(100), nullable=False)
    description = db.Column("sdescripcionplan", db.Text, nullable=True)

    max_users = db.Column("imaxusuarios", db.Integer, nullable=True)
    max_storage_gb = db.Column("imaxalmacenamientogb", db.Integer, nullable=True)

    support_level = db.Column("snivelsoporteplan", db.String(50), nullable=True)       # Basic, Priority, 24/7
    environment_type = db.Column("stipoambienteplan", db.String(30), nullable=True)    # SHARED, DEDICATED

    is_active = db.Column("bactivo", db.Boolean, default=True, nullable=False)
    created_at = db.Column("dcreacion", db.DateTime, default=datetime.utcnow, nullable=False)

    # 🔗 Relación con Lista de Precios
    price_lists = db.relationship(
        "PriceList",
        back_populates="plan",
        lazy=True
    )

    def __repr__(self):
        return f"<Plan {self.code}>"

    def to_dict(self):
        active_price = next(
            (pl for pl in self.price_lists if pl.is_active), 
            None
        )
        
        active_prices_data = [
            pl.to_dict()
            for pl in self.price_lists if pl.is_active
        ]
        #active_price = [pl for pl in self.price_lists if pl.is_active]
        created_at = format_datetime_user(self.created_at) if self.created_at else None
        
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
            "created_at": created_at if self.created_at else None,
            "price_info": active_prices_data
        }
