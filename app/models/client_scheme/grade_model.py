from app import db
from datetime import datetime

class Grade(db.Model):
    __tablename__ = 'notas'
    __table_args__ = {'schema': 'cliente'}

    # Primary Key
    id = db.Column('idnota', db.Integer, primary_key=True)

    # Foreign Keys & Data
    studentCycleClassroomId = db.Column('idestudianteaulacic', db.Integer, nullable=False)
    subjectId = db.Column('idasignatura', db.Integer, nullable=False)
    partialId = db.Column('idparcial', db.Integer, nullable=False)
    grade = db.Column('nnota', db.Numeric(5, 2))
    
    # Audit info (optional but good practice)
    createdAt = db.Column('dfechaqm', db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column('dfecham', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'studentCycleClassroomId': self.studentCycleClassroomId,
            'partialId': self.partialId,
            'grade': float(self.grade) if self.grade is not None else 0.0,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None
        }
