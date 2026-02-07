from app import db

class Classroom(db.Model):
    __tablename__ = 'aulas'
    __table_args__ = {'schema': 'cliente'}

    id = db.Column("idaula", db.Integer, primary_key=True, autoincrement=True)
    courseId = db.Column("idcurso", db.SmallInteger, db.ForeignKey('cliente.cursos.idcurso'), nullable=False)
    name = db.Column("saula", db.String(2), nullable=False)
    maxCapacity = db.Column("icapacidadmaxima", db.SmallInteger, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "courseId": self.courseId,
            "name": self.name,
            "maxCapacity": self.maxCapacity
        }
