from app import db

class SubCycleListView(db.Model):
    __tablename__ = 'vlistasubciclos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idsubciclo", db.Integer, primary_key=True)

    # Columns
    name = db.Column("ssubciclo", db.String)
    order = db.Column("iordensubcic", db.Integer)
    
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    isCycleActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "isCycleActive": self.isCycleActive
        }
