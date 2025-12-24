from app import db


class DynamicField(db.Model):
    """Define qué campos dinámicos existen para cada tipo de entidad"""
    __tablename__ = "dynamic_fields"
    __table_args__ = {"schema": "master"}

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50))  # 'STUDENT', 'TEACHER', 'CLIENT'
    label = db.Column(db.String(100))       # 'Fecha de Graduación'
    name = db.Column(db.String(50))        # 'graduation_date' (la llave en el JSON)
    field_type = db.Column(db.String(20))   # 'TEXT', 'NUMBER', 'DATE', 'SELECT'
    is_required = db.Column(db.Boolean, default=False)
    options = db.Column(db.JSON, nullable=True) # Para campos tipo 'SELECT' (ej: ['A', 'B'])