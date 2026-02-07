from app.extensions import db
from app.models.master_scheme.payment_processor_model import PaymentProcessor

def get_payment_processors():
    return PaymentProcessor.query.all()

def get_payment_processor_by_id(pp_id):
    return PaymentProcessor.query.get(pp_id)

def create_payment_processor(data):
    pp = PaymentProcessor(**data)
    db.session.add(pp)
    db.session.commit()
    return pp

def update_payment_processor(pp_id, data):
    pp = PaymentProcessor.query.get(pp_id)
    if pp:
        for key, value in data.items():
            setattr(pp, key, value)
        db.session.commit()
    return pp

def delete_payment_processor(pp_id):
    pp = PaymentProcessor.query.get(pp_id)
    if pp:
        db.session.delete(pp)
        db.session.commit()
        return True
    return False
