from app import db

class MonthName(db.Model):
    __tablename__ = 'nombremes'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idnombremes', db.Integer, primary_key=True, autoincrement=True)
    month_num = db.Column('inummes', db.Integer, nullable=False, unique=True)
    name = db.Column('snombremes', db.String(20), nullable=False)
    short_name = db.Column('snombresmescorto', db.String(5), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "month_num": self.month_num,
            "name": self.name,
            "short_name": self.short_name
        }
