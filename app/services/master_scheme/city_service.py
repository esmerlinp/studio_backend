from typing import List, Optional
from app import db
from app.models.master_scheme.city_model import City

def create_city(*, name: str, country_id: int, is_active: bool = True) -> City:
    city = City(name=name, country_id=country_id, is_active=is_active)
    try:
        db.session.add(city)
        db.session.commit()
        return city
    except Exception:
        db.session.rollback()
        raise

def get_cities(active_only: bool = False, country_id: Optional[int] = None) -> List[City]:
    query = City.query
    if active_only:
        query = query.filter_by(is_active=True)
    if country_id:
        query = query.filter_by(country_id=country_id)
    return query.order_by(City.name.asc()).all()

def get_city_by_id(city_id: int) -> Optional[City]:
    return City.query.get(city_id)

def update_city(city_id: int, *, name: Optional[str] = None, country_id: Optional[int] = None, is_active: Optional[bool] = None) -> Optional[City]:
    city = City.query.get(city_id)
    if not city:
        return None
    if name is not None:
        city.name = name
    if country_id is not None:
        city.country_id = country_id
    if is_active is not None:
        city.is_active = is_active
    try:
        db.session.commit()
        return city
    except Exception:
        db.session.rollback()
        raise

def delete_city(city_id: int) -> bool:
    city = City.query.get(city_id)
    if not city:
        return False
    try:
        db.session.delete(city)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
