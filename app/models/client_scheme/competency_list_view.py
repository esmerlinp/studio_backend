from app import db

class CompetencyListView(db.Model):
    __tablename__ = 'vlistacompetencias'
    __table_args__ = {'info': dict(is_view=True)}

    # Primary Key
    id = db.Column("idcompetencia", db.Integer, primary_key=True)

    # Columns
    name = db.Column("scompetencia", db.String)
    description = db.Column("sdescripcion", db.String)
    ordering = db.Column("iorden", db.Integer)
    isActive = db.Column("bactivo", db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ordering": self.ordering,
            "isActive": self.isActive
        }
