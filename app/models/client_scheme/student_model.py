from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from app import db # Asegúrate de importar tu instancia de SQLAlchemy

class Student(db.Model):
    __tablename__ = "estudiantes"



    # --- CAMPOS FIJOS (Mapeo SQL -> Python) ---
    
    id = db.Column("idestudiante", db.Integer, primary_key=True)
    
    request_id = db.Column("idsolicitud", db.Integer, 
        db.ForeignKey("cliente.solicitudes.idsolicitud"), nullable=True)
    
    student_code = db.Column("scodigoestudiante", db.String(25), nullable=False)
    
    enrollment_date = db.Column("dfechainscripcion", db.Date, 
        nullable=False, default=datetime.utcnow)
    
    last_name1 = db.Column("sestapellido1", db.String(25), nullable=False)
    last_name2 = db.Column("sestapellido2", db.String(25), nullable=True)
    
    first_name1 = db.Column("sestnombre1", db.String(50), nullable=False)
    first_name2 = db.Column("sestnombre2", db.String(50), nullable=True)
    
    gender_id = db.Column("idsexo", db.Integer, nullable=False)
    
    living_situation = db.Column("ivive", db.SmallInteger, nullable=False)
    
    birth_date = db.Column("dfechanacimiento", db.Date, nullable=False)
    
    country_id = db.Column("idpais", db.Integer, nullable=True)
    city_id = db.Column("idciudad", db.Integer, nullable=True)
    sector_id = db.Column("idsector", db.Integer, nullable=True)
    
    address = db.Column("sdireccion", db.String(300), nullable=True)
    
    previous_school_id = db.Column("idcolegioprocedencia", db.Integer, nullable=True)
    
    entry_reason = db.Column("smotivoentrada", db.Text, nullable=True)
    exit_reason = db.Column("smotivosalida", db.Text, nullable=True)
    
    status = db.Column("iestadoestudiante", db.SmallInteger, 
        nullable=False, default=1) # 1=Activo, 2=Exalumno, 3=Graduado
    
    family_id = db.Column("idestudiantefam", db.Integer, 
        db.ForeignKey("cliente.estudiantesfam.idestudiantefam"), nullable=True)
    
    blood_type_id = db.Column("idtiposangre", db.SmallInteger, nullable=True)
    
    doctor_name = db.Column("snombremedico", db.String(50), nullable=True)
    
    insurance_number = db.Column("snumeroseguromedico", db.String(25), nullable=True)
    
    medical_institution_id = db.Column("idinstitucionmedica", db.SmallInteger, nullable=True)
    
    insurance_institution_id = db.Column("idinstitucionsegmed", db.SmallInteger, nullable=True)

    # --- CAMPO PARA DATOS DINÁMICOS ---
    # Este campo debe ser agregado vía ALTER TABLE antes de usarlo
    custom_attributes = db.Column("jatributos", JSONB, 
        nullable=False, server_default='{}')

    def __repr__(self):
        return f"<Student {self.first_name1} {self.last_name1} (Code: {self.student_code})>"

    def to_dict(self):
        """Convierte el objeto a un diccionario para respuestas JSON"""
        return {
            "id": self.id,
            "student_code": self.student_code,
            "first_name": f"{self.first_name1} {self.first_name2 or ''}".strip(),
            "last_name": f"{self.last_name1} {self.last_name2 or ''}".strip(),
            "enrollment_date": self.enrollment_date.isoformat(),
            "status": self.status,
            # Incluimos los campos dinámicos directamente
            "extra_info": self.custom_attributes 
        }