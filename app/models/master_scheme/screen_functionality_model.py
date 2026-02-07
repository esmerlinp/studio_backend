from ...extensions import db

class ScreenFunctionality(db.Model):
    __tablename__ = "pantallasfuncionalidades"
    __table_args__ = (
        db.UniqueConstraint("idpantalla", "idfuncionalidad", name="uq_pantallasfuncionalidades_pantalla_funcionalidad"),
        {"schema": "master"}
    )

    id = db.Column("idpantallafuncionalidad", db.Integer, primary_key=True)
    screen_id = db.Column("idpantalla", db.Integer, db.ForeignKey("master.pantallas.idpantalla"), nullable=False)
    functionality_id = db.Column("idfuncionalidad", db.Integer, db.ForeignKey("master.funcionalidades.idfuncionalidad"), nullable=False)
    is_active = db.Column("bactivo", db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "screen_id": self.screen_id,
            "functionality_id": self.functionality_id,
            "is_active": self.is_active
        }
