from app import db


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": "master"}

    id = db.Column(
        "idrol",
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        "srol",
        db.String(50),
        nullable=False,
        unique=True,
        index=True
    )
    code = db.Column(
        "scodigo",
        db.String(20),
        nullable=True,
        unique=True,
        index=True,
        default=None
    )

    description = db.Column(
        "sdescripcion",
        db.String(200),
        nullable=True
    )

    is_active = db.Column(
        "bactivo",
        db.Boolean,
        nullable=False,
        default=True
    )


    # ───────────────────────────────────────
    # Utilidades
    # ───────────────────────────────────────
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f"<Role id={self.id} code={self.code}>"
