from datetime import datetime
from ...extensions import db
from app.utils.helpers import format_datetime_user
from sqlalchemy.dialects.postgresql import JSONB

class PriceList(db.Model):
    __tablename__ = "listasprecios"
    __table_args__ = {"schema": "master"}


    id = db.Column("idlistaprecio", db.Integer, primary_key=True)

    plan_id = db.Column("idplan",
        db.Integer,
        db.ForeignKey("master.planes.idplan"),
        nullable=False
    )

    billing_cycle = db.Column(
        "sciclopago", 
        db.String(20),
        nullable=False
    )  # MONTHLY, ANNUAL

    price = db.Column(
        "nprecio", 
        db.Numeric(12, 2),
        nullable=False
    )

    currency = db.Column(
        "smoneda", 
        db.String(10),
        default="USD",
        nullable=False
    )

    price_per_user = db.Column(
        "bprecioportusuario",
        db.Boolean,
        default=False,
        nullable=False
    )

    min_users = db.Column(
        "iminusuarios", 
        db.Integer,
        default=1,
        nullable=False
    )

    valid_from = db.Column(
        "dvalidodesde",
        db.Date,
        nullable=False
    )

    valid_to = db.Column(
        "dvalidohasta",
        db.Date,
        nullable=True
    )

    is_active = db.Column(
        "bactivo",
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        "dcreacion",
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    is_trial = db.Column(
        "btrial",
        db.Boolean,
        default=False,
        nullable=False
    )

    trial_days = db.Column(
        "itrialdias", 
        db.Integer,
        default=0,
        nullable=False
    )
    
    features_config = db.Column('jcaracteristicas', JSONB, nullable=False, default={})

    # 🔗 Relación con Plan
    plan = db.relationship(
        "Plan",
        back_populates="price_lists"
    )

    def __repr__(self):
        return (
            f"<PriceList plan_id={self.plan_id} "
            f"billing_cycle={self.billing_cycle} "
            f"price={self.price} {self.currency}>"
        )

    def to_dict(self):
        created_at = format_datetime_user(self.created_at) if self.created_at else None
        
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "plan_code": self.plan.code if self.plan else None,
            "billing_cycle": self.billing_cycle,
            "price": float(self.price),
            "currency": self.currency,
            "price_per_user": self.price_per_user,
            "min_users": self.min_users,
            "is_trial": self.is_trial,
            "trial_days": self.trial_days,
            "valid_from": self.valid_from.isoformat(),
            "valid_to": self.valid_to.isoformat() if self.valid_to else None,
            "is_active": self.is_active,
            "created_at": created_at if self.created_at else None,
            "features_config":self.features_config
        }
