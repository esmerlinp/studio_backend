from app import db

class CycleListView(db.Model):
    __tablename__ = 'vlistaciclos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idciclo", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sciclo", db.String)
    startDate = db.Column("dfechainicio", db.Date)
    endDate = db.Column("dfechafin", db.Date)
    isActive = db.Column("bactivo", db.Boolean)
    subCycleCount = db.Column("ncantsubciclos", db.Integer)
    studentCount = db.Column("ncantestudiantes", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "isActive": self.isActive,
            "subCycleCount": int(self.subCycleCount) if self.subCycleCount is not None else 0,
            "studentCount": int(self.studentCount) if self.studentCount is not None else 0
        }
