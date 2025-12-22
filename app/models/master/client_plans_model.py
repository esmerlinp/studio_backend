from datetime import datetime
from ...extensions import db


class ClientPlan(db.Model):
    __tablename__ = "client_plans"

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    plan_id = db.Column(
        db.Integer,
        db.ForeignKey("plans.id"),
        nullable=False
    )

    price_list_id = db.Column(
        db.Integer,
        db.ForeignKey("price_lists.id"),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE",
        nullable=False
    )  # ACTIVE, SUSPENDED, CANCELED, EXPIRED

    # 🔗 Relaciones
    plan = db.relationship(
        "Plan",
        backref=db.backref("client_plans", lazy=True)
    )

    price_list = db.relationship(
        "PriceList",
        backref=db.backref("client_plans", lazy=True)
    )

    def __repr__(self):
        return (
            f"<ClientPlan client_id={self.client_id} "
            f"plan={self.plan.code if self.plan else None} "
            f"status={self.status}>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "plan_id": self.plan_id,
            "plan_code": self.plan.code if self.plan else None,
            "price_list_id": self.price_list_id,
            "billing_cycle": self.price_list.billing_cycle if self.price_list else None,
            "price": float(self.price_list.price) if self.price_list else None,
            "currency": self.price_list.currency if self.price_list else None,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
        }
