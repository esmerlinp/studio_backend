from app import db

class SubjectAreaListView(db.Model):
    __tablename__ = 'vlistaareastematicas'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idareatematica", db.Integer, primary_key=True)

    # Columns
    name = db.Column("sareatematica", db.String)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "isActive": self.isActive
        }
