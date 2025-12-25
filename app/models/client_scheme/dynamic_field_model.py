from ...extensions import db


class DynamicField(db.Model):
    """Define qué campos dinámicos existen para cada tipo de entidad"""
    __tablename__ = "camposdinamicos"

    # --- CAMPOS FIJOS (CamelCase) ---
    id = db.Column("idcampodinamico", db.Integer, primary_key=True)
    entityType = db.Column("stipoentidad", db.String(50))  # 'STUDENT', 'TEACHER', etc.
    label = db.Column("setiqueta", db.String(100))        # 'Fecha de Graduación'
    name = db.Column("snombrecampo", db.String(50))       # 'graduation_date'
    fieldType = db.Column("stipocampo", db.String(20))    # 'TEXT', 'NUMBER', 'DATE', 'SELECT'
    isRequired = db.Column("brequerido", db.Boolean, default=False)
    options = db.Column("jopciones", db.JSON, nullable=True) # ['Opción A', 'Opción B']

    def __repr__(self):
        return f"<DynamicField {self.name} for {self.entityType}>"

    def to_dict(self):
        """
        Convierte la definición del campo dinámico a un diccionario.
        Útil para que el Frontend sepa qué inputs debe renderizar.
        """
        return {
            "id": self.id,
            "entityType": self.entityType,
            "label": self.label,
            "name": self.name,
            "fieldType": self.fieldType,
            "isRequired": self.isRequired,
            "options": self.options  # Se mantiene como JSON original
        }