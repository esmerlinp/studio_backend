from app import db
from datetime import datetime

class Storage(db.Model):
    __tablename__ = 'almacenamiento'


    id = db.Column("idalmacenamiento", db.Integer, primary_key=True)
    client_id = db.Column("idcliente", db.Integer, nullable=False) # ID del Cliente
    
    # Relación Polimórfica
    entity = db.Column("sentidadtipo", db.String(50), nullable=False) # Ej: 'ESTUDIANTE'
    record_id = db.Column("sentidadid", db.String(50), nullable=False)   # UUID o ID del registro

    # Datos del Archivo en GCS
    file_name = db.Column("snombreoriginal", db.String(255), nullable=False)
    path_gcs = db.Column("sruta_gcs", db.Text, nullable=False)
    generation_id = db.Column("sgeneration_id", db.String(50))
    content_type = db.Column("scontent_type", db.String(100))
    peso_mb = db.Column("npeso_mb", db.Numeric(10, 2))

    created_at = db.Column("dfechacreacion", db.DateTime, default=datetime.utcnow)
    updated_at = db.Column("dfechamodificacion", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column("dfechaeliminacion", db.DateTime) # Para Soft Delete (Opcional)


    def to_dict(self, show_confidencial=False):
            """Convierte el objeto a un diccionario para respuestas JSON"""
            data = {
                "id": self.id,
                "client_id": self.client_id,
                "entity": self.entity,
                "record_id": self.record_id,
                "file_name": self.file_name,
                "content_type": self.content_type,
                "peso_mb": float(self.peso_mb) if self.peso_mb else 0.0,
                "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
                "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
                "is_deleted": self.deleted_at is not None
            }
            
            if show_confidencial:
                data["path_gcs"] = self.path_gcs
                data["generation_id"] = self.generation_id
            
            return data