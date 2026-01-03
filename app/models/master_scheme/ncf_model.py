from ...extensions import db

class NCFSequence(db.Model):
    __tablename__ = 'ncf'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idsecuencia', db.Integer, primary_key=True)
    type_ncf = db.Column('stiponcf', db.String(3), nullable=False) # '01' para Crédito Fiscal, '02' Consumidor Final
    prefix = db.Column('sprefijo', db.String(1), default='B')
    current_number = db.Column('inumeroactual', db.Integer, default=1)
    max_number = db.Column('inumeromaximo', db.Integer)
    is_active = db.Column('bactivo', db.Boolean, default=True)

    def get_next_ncf(self):
        # Genera el string formateado: B0100000001
        formatted_number = str(self.current_number).zfill(8)
        ncf = f"{self.prefix}{self.type_ncf}{formatted_number}"
        return ncf

class NCFLog(db.Model):
    __tablename__ = 'ncflog'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idlog', db.Integer, primary_key=True)
    client_id = db.Column('idcliente', db.Integer, db.ForeignKey('master.clientes.idcliente'))
    ncf_assigned = db.Column('sncfasignado', db.String(11))
    stripe_invoice_id = db.Column('stripe_invoice_id', db.String(50))
    created_at = db.Column('dfechacreacion', db.DateTime, default=db.func.current_timestamp())