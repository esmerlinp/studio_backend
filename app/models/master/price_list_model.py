from datetime import datetime
from ...extensions import db


class PriceList(db.Model):
    __tablename__ = "price_lists"

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(
        db.Integer,
        db.ForeignKey("plans.id"),
        nullable=False
    )

    billing_cycle = db.Column(
        db.String(20),
        nullable=False
    )  # MONTHLY, ANNUAL

    price = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    currency = db.Column(
        db.String(10),
        default="USD",
        nullable=False
    )

    price_per_user = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    min_users = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    valid_from = db.Column(
        db.Date,
        nullable=False
    )

    valid_to = db.Column(
        db.Date,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # 🔗 Relación con Plan
    plan = db.relationship(
        "Plan",
        backref=db.backref("price_lists", lazy=True)
    )

    def __repr__(self):
        return (
            f"<PriceList plan_id={self.plan_id} "
            f"billing_cycle={self.billing_cycle} "
            f"price={self.price} {self.currency}>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "plan_code": self.plan.code if self.plan else None,
            "billing_cycle": self.billing_cycle,
            "price": float(self.price),
            "currency": self.currency,
            "price_per_user": self.price_per_user,
            "min_users": self.min_users,
            "valid_from": self.valid_from.isoformat(),
            "valid_to": self.valid_to.isoformat() if self.valid_to else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
