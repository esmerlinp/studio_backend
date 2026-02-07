from app import db

class ScheduleBlockListView(db.Model):
    __tablename__ = 'vlistabloqueshorarios'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idbloquehorario", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sbloquehorario", db.String)
    isActive = db.Column("bactivo", db.Boolean)
    totalActiveBlocks = db.Column("itotalbloquesactivos", db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "isActive": self.isActive,
            "totalActiveBlocks": int(self.totalActiveBlocks) if self.totalActiveBlocks is not None else 0
        }
