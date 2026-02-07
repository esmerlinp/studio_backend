from typing import List, Optional
from app import db
from app.models.master_scheme.bank_model import Bank

def create_bank(*, name: str, is_active: bool = True) -> Bank:
    bank = Bank(name=name, is_active=is_active)
    
    try:
        db.session.add(bank)
        db.session.commit()
        return bank
    except Exception:
        db.session.rollback()
        raise

def get_banks(active_only: bool = False) -> List[Bank]:
    query = Bank.query
    if active_only:
        query = query.filter_by(is_active=True)
    return query.order_by(Bank.name.asc()).all()

def get_bank_by_id(bank_id: int) -> Optional[Bank]:
    return Bank.query.get(bank_id)

def update_bank(bank_id: int, *, name: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[Bank]:
    bank = Bank.query.get(bank_id)
    if not bank:
        return None

    if name is not None:
        bank.name = name
    if is_active is not None:
        bank.is_active = is_active

    try:
        db.session.commit()
        return bank
    except Exception:
        db.session.rollback()
        raise

def deactivate_bank(bank_id: int) -> bool:
    bank = Bank.query.get(bank_id)
    if not bank:
        return False
    
    bank.is_active = False
    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise

def delete_bank(bank_id: int) -> bool:
    bank = Bank.query.get(bank_id)
    if not bank:
        return False
    
    try:
        db.session.delete(bank)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
