from app import db

class CycleLevelScheduleBlockView(db.Model):
    __tablename__ = 'vlistaciclosnivbloqhor'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idciclonivbloqhor", db.Integer, primary_key=True)

    # Columns
    cycleId = db.Column("idciclo", db.Integer)
    cycleName = db.Column("sciclo", db.String)
    
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    
    scheduleBlockId = db.Column("idbloquehorario", db.Integer)
    scheduleBlockName = db.Column("sbloquehorario", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "cycleId": self.cycleId,
            "cycleName": self.cycleName,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "scheduleBlockId": self.scheduleBlockId,
            "scheduleBlockName": self.scheduleBlockName
        }
