import datetime
from app import db


class ClienteConfiguracion(db.Model):
    __tablename__ = "cliente_configuracion"

    id = db.Column(db.Integer, primary_key=True)

    idcliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # ======================
    # Seguridad
    # ======================
    idle_timeout_minutes = db.Column(db.Integer, default=30)
    password_expiration_days = db.Column(db.Integer, default=90)
    max_login_attempts = db.Column(db.Integer, default=5)
    auto_unlock_minutes = db.Column(db.Integer, default=30)
    refresh_token_expiration_days = db.Column(db.Integer, default=7)
    enforce_2fa = db.Column(db.Boolean, default=False)

    # ======================
    # Sistema
    # ======================
    timezone = db.Column(db.String(100), default="America/Santo_Domingo")
    language = db.Column(db.String(10), default="es")
    date_format = db.Column(db.String(20), default="DD/MM/YYYY")

    # ======================
    # Personalización
    # ======================
    company_logo_url = db.Column(db.Text)
    primary_color = db.Column(db.String(20))
    secondary_color = db.Column(db.String(20))

    # ======================
    # Límites y plan
    # ======================
    plan = db.Column(db.String(20), default="standard")
    max_users = db.Column(db.Integer, default=50)

    modules_enabled = db.Column(
        db.JSON,
        default=lambda: {
            "academico": True,
            "enfermeria": True,
            "cafeteria": True,
            "financiero": True,
            "padres": True,
        }
    )

    # ======================
    # Integraciones
    # ======================
    smtp_server = db.Column(db.String(255))
    smtp_port = db.Column(db.Integer)
    smtp_username = db.Column(db.String(255))
    smtp_password = db.Column(db.Text)

    api_keys = db.Column(db.JSON)
    webhooks = db.Column(db.JSON)

    # ======================
    # Auditoría
    # ======================
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ======================
    # Helpers
    # ======================
    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "idcliente": self.idcliente,

            # Seguridad
            "idle_timeout_minutes": self.idle_timeout_minutes,
            "password_expiration_days": self.password_expiration_days,
            "max_login_attempts": self.max_login_attempts,
            "auto_unlock_minutes": self.auto_unlock_minutes,
            "refresh_token_expiration_days": self.refresh_token_expiration_days,
            "enforce_2fa": self.enforce_2fa,

            # Sistema
            "timezone": self.timezone,
            "language": self.language,
            "date_format": self.date_format,

            # Personalización
            "company_logo_url": self.company_logo_url,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,

            # Límites y plan
            "plan": self.plan,
            "max_users": self.max_users,
            "modules_enabled": self.modules_enabled,

            # Integraciones
            "smtp_server": self.smtp_server,
            # ❌ smtp_password NO se expone
            "api_keys": self.api_keys,
            "webhooks": self.webhooks,

            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_sensitive:
            data['smtp_password'] = self.smtp_password
        
        return data
