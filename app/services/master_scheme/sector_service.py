from app.extensions import db
from app.models.master_scheme.sector_model import Sector

def get_sectors():
    return Sector.query.all()

def get_sector_by_id(sector_id):
    return Sector.query.get(sector_id)

def create_sector(data):
    sector = Sector(**data)
    db.session.add(sector)
    db.session.commit()
    return sector

def update_sector(sector_id, data):
    sector = Sector.query.get(sector_id)
    if sector:
        for key, value in data.items():
            setattr(sector, key, value)
        db.session.commit()
    return sector

def delete_sector(sector_id):
    sector = Sector.query.get(sector_id)
    if sector:
        db.session.delete(sector)
        db.session.commit()
        return True
    return False
