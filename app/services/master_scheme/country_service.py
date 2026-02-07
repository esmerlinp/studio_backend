from typing import List, Optional
from app import db
from app.models.master_scheme.country_model import Country

def get_countries(active_only: bool = False) -> List[Country]:
    query = Country.query
    if active_only:
        query = query.filter(Country.is_active == True)
    return query.order_by(Country.name.asc()).all()

def get_country_by_id(country_id: int) -> Optional[Country]:
    return Country.query.get(country_id)

def create_country(*, name: str, iso_code: str, is_active: bool = True) -> Country:
    country = Country(name=name, iso_code=iso_code, is_active=is_active)
    db.session.add(country)
    try:
        db.session.commit()
        return country
    except Exception as e:
        db.session.rollback()
        raise e

def update_country(country_id: int, **kwargs) -> Optional[Country]:
    country = get_country_by_id(country_id)
    if not country:
        return None
    
    for key, value in kwargs.items():
        if hasattr(country, key) and value is not None:
            setattr(country, key, value)
    
    try:
        db.session.commit()
        return country
    except Exception as e:
        db.session.rollback()
        raise e

def delete_country(country_id: int) -> bool:
    country = get_country_by_id(country_id)
    if not country:
        return False
    db.session.delete(country)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
