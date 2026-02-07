from app import db

class SubjectListView(db.Model):
    __tablename__ = 'vlistaasignaturas'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idasignatura", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sasignatura", db.String)
    subjectAreaId = db.Column("idareatematica", db.Integer)
    subjectAreaName = db.Column("sareatematica", db.String)
    ordering = db.Column("iorden", db.Integer)
    credits = db.Column("icreditos", db.Integer)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "subjectAreaId": self.subjectAreaId,
            "subjectAreaName": self.subjectAreaName,
            "ordering": self.ordering,
            "credits": self.credits,
            "isActive": self.isActive
        }
