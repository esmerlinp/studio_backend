from app import db

class FamilyListView(db.Model):
    __tablename__ = 'vlistasolicitudesfam'
    __table_args__ = {'info': dict(is_view=True)}

    id = db.Column("idestudiantefam", db.Integer, primary_key=True)
    familyCode = db.Column("scodfam", db.String)
    fatherName = db.Column("spadre", db.String)
    motherName = db.Column("smadre", db.String)
    tutorName = db.Column("stutor", db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "familyCode": self.familyCode,
            "fatherName": self.fatherName,
            "motherName": self.motherName,
            "tutorName": self.tutorName
        }
