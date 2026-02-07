from app import db

class ConceptListView(db.Model):
    __tablename__ = 'vlistaconceptos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idconcepto", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sconcepto", db.String)
    isFamily = db.Column("bfamiliar", db.Boolean)
    isRecurrent = db.Column("brecurrente", db.Boolean)
    isActive = db.Column("bactivo", db.Boolean)
    appliesDiscount = db.Column("baplicadescuento", db.Boolean)
    appliesSurcharge = db.Column("baplicarecargo", db.Boolean)
    appliesItbis = db.Column("baplicaitbis", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "isFamily": self.isFamily,
            "isRecurrent": self.isRecurrent,
            "isActive": self.isActive,
            "appliesDiscount": self.appliesDiscount,
            "appliesSurcharge": self.appliesSurcharge,
            "appliesItbis": self.appliesItbis
        }
