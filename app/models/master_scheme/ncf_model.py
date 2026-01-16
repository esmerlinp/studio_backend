from ...extensions import db
from app.utils.helpers import format_datetime_user

class NCFSequence(db.Model):
    __tablename__ = 'ncf'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idsecuencia', db.Integer, primary_key=True)
    type_ncf = db.Column('stiponcf', db.String(3), nullable=False) # '01' para Crédito Fiscal, '02' Consumidor Final
    prefix = db.Column('sprefijo', db.String(1), default='B')
    current_number = db.Column('inumeroactual', db.Integer, default=1)
    max_number = db.Column('inumeromaximo', db.Integer)
    is_active = db.Column('bactivo', db.Boolean, default=True)
    expiration_date = db.Column('dfechavencimiento', db.Date, nullable=True)

    def get_next_ncf(self):
        # Genera el string formateado: B0100000001
        formatted_number = str(self.current_number).zfill(8)
        ncf = f"{self.prefix}{self.type_ncf}{formatted_number}"
        return ncf

    def to_dict(self):
        expiration_date = format_datetime_user(self.expiration_date) if self.expiration_date else None
        return {
            "id": self.id,
            "type_ncf": self.type_ncf,
            "prefix": self.prefix,
            "current_number": self.current_number,
            "max_number": self.max_number,
            "is_Active": self.is_active,
            "expiration_date": expiration_date
        }
        
class NCFLog(db.Model):
    __tablename__ = 'ncflog'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idlog', db.Integer, primary_key=True)
    client_id = db.Column('idcliente', db.Integer, db.ForeignKey('master.clientes.idcliente'))
    ncf_assigned = db.Column('sncfasignado', db.String(11))
    stripe_invoice_id = db.Column('stripe_invoice_id', db.String(50))
    created_at = db.Column('dfechacreacion', db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        created_at = format_datetime_user(self.created_at) if self.created_at else None
        return {
            "id":self.id,
            "client_id": self.client_id,
            "ncf_assigned": self.ncf_assigned,
            "stripe_invoice_id":self.stripe_invoice_id,
            "create_at":created_at
        }