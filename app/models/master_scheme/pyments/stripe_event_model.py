from ....extensions import db
from datetime import datetime, timezone

class StripeEventLog(db.Model):
    __tablename__ = 'stripe_event_log'
    __table_args__ = {"schema": "master"}

    id = db.Column(db.Integer, primary_key=True)
    stripe_event_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    event_type = db.Column(db.String(100))
    processed_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<StripeEventLog {self.stripe_event_id}>'
