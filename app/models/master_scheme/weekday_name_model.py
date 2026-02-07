from app import db

class WeekdayName(db.Model):
    __tablename__ = 'nombresem'
    __table_args__ = {'schema': 'master'}

    id = db.Column('idnombresem', db.Integer, primary_key=True, autoincrement=True)
    weekday_num = db.Column('inumsem', db.Integer, nullable=False, unique=True)
    name = db.Column('snombresem', db.String(20), nullable=False)
    short_name = db.Column('snombresemcorto', db.String(5), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "weekday_num": self.weekday_num,
            "name": self.name,
            "short_name": self.short_name
        }
