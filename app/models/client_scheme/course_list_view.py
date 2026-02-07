from app import db

class CourseListView(db.Model):
    __tablename__ = 'vlistacursos'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idcurso", db.Integer, primary_key=True)

    # Columns
    name = db.Column("scurso", db.String)
    levelId = db.Column("idnivel", db.Integer)
    levelName = db.Column("snivel", db.String)
    averageAge = db.Column("iedadpromedio", db.Integer)
    
    nextCourseId = db.Column("idcursosiguiente", db.Integer)
    nextCourseName = db.Column("scursosiguiente", db.String)
    
    ordering = db.Column("iorden", db.Integer)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "levelId": self.levelId,
            "levelName": self.levelName,
            "averageAge": self.averageAge,
            "nextCourseId": self.nextCourseId,
            "nextCourseName": self.nextCourseName,
            "ordering": self.ordering,
            "isActive": self.isActive
        }
