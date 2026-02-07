from app import db

class LevelListView(db.Model):
    __tablename__ = 'vlistaniveles'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idnivel", db.Integer, primary_key=True)

    # Columns
    name = db.Column("snivel", db.String)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "isActive": self.isActive
        }
