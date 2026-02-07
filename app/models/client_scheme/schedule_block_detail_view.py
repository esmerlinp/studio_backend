from app import db

class ScheduleBlockDetailView(db.Model):
    __tablename__ = 'vdetallebloqueshorarios'
    __table_args__ = {'info': dict(is_view=True)}

    # Composite PK
    scheduleBlockId = db.Column("idbloquehorario", db.Integer, primary_key=True)
    rowNumber = db.Column("inumerofila", db.Integer, primary_key=True)

    # Columns
    scheduleBlockName = db.Column("sbloquehorario", db.String)
    isActive = db.Column("bactivo", db.Boolean)
    
    startTime = db.Column("thorainicio", db.Time)
    endTime = db.Column("thorafin", db.Time)
    
    isMonday = db.Column("blunes", db.Boolean)
    isTuesday = db.Column("bmartes", db.Boolean)
    isWednesday = db.Column("bmiercoles", db.Boolean)
    isThursday = db.Column("bjueves", db.Boolean)
    isFriday = db.Column("bviernes", db.Boolean)
    isSaturday = db.Column("bsabado", db.Boolean)
    isSunday = db.Column("bdomingo", db.Boolean)

    def to_dict(self):
        return {
            "scheduleBlockId": self.scheduleBlockId,
            "scheduleBlockName": self.scheduleBlockName,
            "isActive": self.isActive,
            "rowNumber": self.rowNumber,
            "startTime": self.startTime.strftime("%H:%M:%S") if self.startTime else None,
            "endTime": self.endTime.strftime("%H:%M:%S") if self.endTime else None,
            "isMonday": self.isMonday,
            "isTuesday": self.isTuesday,
            "isWednesday": self.isWednesday,
            "isThursday": self.isThursday,
            "isFriday": self.isFriday,
            "isSaturday": self.isSaturday,
            "isSunday": self.isSunday
        }
