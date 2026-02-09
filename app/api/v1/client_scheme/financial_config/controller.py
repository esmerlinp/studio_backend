from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.client_scheme.payment_frequency_list_view import PaymentFrequencyListView

@jwt_required()
def get_frequencies():
    frequencies = PaymentFrequencyListView.query.order_by(PaymentFrequencyListView.id).all()
    return jsonify([f.to_dict() for f in frequencies]), 200

@jwt_required()
def get_frequency(id):
    frequency = PaymentFrequencyListView.query.get(id)
    if not frequency:
        return jsonify({'message': 'Frecuencia no encontrada'}), 404
    return jsonify(frequency.to_dict()), 200

# Note: PaymentFrequencyListView is a view, so it's read-only.
# We need the underlying table model to perform writes.
# Assuming the table is 'cliente.tfrecuenciaspagos' based on naming convention.
# Since I only saw the view model, I will create a basic table model here for CRUD.

from sqlalchemy import Integer, String, Boolean
class PaymentFrequencyModel(db.Model):
    __tablename__ = 'tfrecuenciaspago'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idfrecuenciapago", Integer, primary_key=True)
    frequencyName = db.Column("sfrecuenciapago", String)
    paymentCount = db.Column("icantpagos", Integer)
    isActive = db.Column("bactivo", Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "frequencyName": self.frequencyName,
            "paymentCount": self.paymentCount,
            "isActive": self.isActive
        }

@jwt_required()
def create_frequency():
    data = request.json
    try:
        new_freq = PaymentFrequencyModel(
            frequencyName=data.get('frequencyName'),
            paymentCount=data.get('paymentCount'),
            isActive=data.get('isActive', True)
        )
        db.session.add(new_freq)
        db.session.commit()
        return jsonify(new_freq.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_frequency(id):
    data = request.json
    try:
        freq = PaymentFrequencyModel.query.get(id)
        if not freq:
            return jsonify({'message': 'Frecuencia no encontrada'}), 404
            
        freq.frequencyName = data.get('frequencyName', freq.frequencyName)
        freq.paymentCount = data.get('paymentCount', freq.paymentCount)
        freq.isActive = data.get('isActive', freq.isActive)
        
        db.session.commit()
        return jsonify(freq.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_frequency(id):
    try:
        freq = PaymentFrequencyModel.query.get(id)
        if not freq:
            return jsonify({'message': 'Frecuencia no encontrada'}), 404
            
        # Logical delete preferred? Or physical? Assuming physical for now based on button
        db.session.delete(freq)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# School Cycles Logic
# ---------------------------------------------------------------------------

from app.models.client_scheme.cycle_list_view import CycleListView
from sqlalchemy import Date

class SchoolCycleModel(db.Model):
    __tablename__ = 'tciclos'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idciclo", Integer, primary_key=True)
    name = db.Column("sciclo", String)
    startDate = db.Column("dfechainicio", Date)
    endDate = db.Column("dfechafin", Date)
    isActive = db.Column("bactivo", Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "startDate": self.startDate.isoformat() if self.startDate else None,
            "endDate": self.endDate.isoformat() if self.endDate else None,
            "isActive": self.isActive
        }

@jwt_required()
def get_cycles():
    cycles = CycleListView.query.order_by(CycleListView.id.desc()).all()
    return jsonify([c.to_dict() for c in cycles]), 200

@jwt_required()
def get_cycle(id):
    cycle = CycleListView.query.get(id)
    if not cycle:
        return jsonify({'message': 'Ciclo no encontrado'}), 404
    return jsonify(cycle.to_dict()), 200

@jwt_required()
def create_cycle():
    data = request.json
    try:
        # If setting active, deactivate others (optional logic, but common)
        if data.get('isActive'):
            SchoolCycleModel.query.filter_by(isActive=True).update({'isActive': False})
            
        new_cycle = SchoolCycleModel(
            name=data.get('name'),
            startDate=data.get('startDate'),
            endDate=data.get('endDate'),
            isActive=data.get('isActive', False)
        )
        db.session.add(new_cycle)
        db.session.commit()
        return jsonify(new_cycle.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_cycle(id):
    data = request.json
    try:
        cycle = SchoolCycleModel.query.get(id)
        if not cycle:
            return jsonify({'message': 'Ciclo no encontrado'}), 404
            
        if data.get('isActive') and not cycle.isActive:
             SchoolCycleModel.query.filter(SchoolCycleModel.id != id).update({'isActive': False})
            
        cycle.name = data.get('name', cycle.name)
        cycle.startDate = data.get('startDate', cycle.startDate)
        cycle.endDate = data.get('endDate', cycle.endDate)
        cycle.isActive = data.get('isActive', cycle.isActive)
        
        db.session.commit()
        return jsonify(cycle.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# Payment Concepts Logic
# ---------------------------------------------------------------------------

from app.models.client_scheme.concept_list_view import ConceptListView

class PaymentConceptModel(db.Model):
    __tablename__ = 'tconceptos'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idconcepto", Integer, primary_key=True)
    name = db.Column("sconcepto", String)
    isFamily = db.Column("bfamiliar", Boolean)
    isRecurrent = db.Column("brecurrente", Boolean)
    isActive = db.Column("bactivo", Boolean, default=True)
    appliesDiscount = db.Column("baplicadescuento", Boolean)
    appliesSurcharge = db.Column("baplicarecargo", Boolean)
    appliesItbis = db.Column("baplicaitbis", Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "isFamily": self.isFamily,
            "isRecurrent": self.isRecurrent,
            "isActive": self.isActive,
            "appliesDiscount": self.appliesDiscount,
            "appliesSurcharge": self.appliesSurcharge,
            "appliesItbis": self.appliesItbis
        }

@jwt_required()
def get_concepts():
    concepts = ConceptListView.query.order_by(ConceptListView.id).all()
    return jsonify([c.to_dict() for c in concepts]), 200

@jwt_required()
def get_concept(id):
    concept = ConceptListView.query.get(id)
    if not concept:
        return jsonify({'message': 'Concepto no encontrado'}), 404
    return jsonify(concept.to_dict()), 200

@jwt_required()
def create_concept():
    data = request.json
    try:
        new_concept = PaymentConceptModel(
            name=data.get('name'),
            isFamily=data.get('isFamily', False),
            isRecurrent=data.get('isRecurrent', False),
            isActive=data.get('isActive', True),
            appliesDiscount=data.get('appliesDiscount', False),
            appliesSurcharge=data.get('appliesSurcharge', False),
            appliesItbis=data.get('appliesItbis', False)
        )
        db.session.add(new_concept)
        db.session.commit()
        return jsonify(new_concept.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_concept(id):
    data = request.json
    try:
        concept = PaymentConceptModel.query.get(id)
        if not concept:
            return jsonify({'message': 'Concepto no encontrado'}), 404
            
        concept.name = data.get('name', concept.name)
        concept.isFamily = data.get('isFamily', concept.isFamily)
        concept.isRecurrent = data.get('isRecurrent', concept.isRecurrent)
        concept.isActive = data.get('isActive', concept.isActive)
        concept.appliesDiscount = data.get('appliesDiscount', concept.appliesDiscount)
        concept.appliesSurcharge = data.get('appliesSurcharge', concept.appliesSurcharge)
        concept.appliesItbis = data.get('appliesItbis', concept.appliesItbis)
        
        db.session.commit()
        return jsonify(concept.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_concept(id):
    try:
        concept = PaymentConceptModel.query.get(id)
        if not concept:
            return jsonify({'message': 'Concepto no encontrado'}), 404
        db.session.delete(concept)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# Course Costs Logic
# ---------------------------------------------------------------------------

from app.models.client_scheme.course_list_view import CourseListView

class CourseCostModel(db.Model):
    __tablename__ = 'tcostoscurso'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idcostocurso", Integer, primary_key=True)
    cycleId = db.Column("idciclo", Integer)
    courseId = db.Column("idcurso", Integer)
    conceptId = db.Column("idconcepto", Integer)
    amount = db.Column("nmonto", db.Numeric)
    isActive = db.Column("bactivo", Boolean, default=True)

    def to_dict(self):
        # Fetch related names for display (in a real scenario, use joins or relationship properties)
        cycle = CycleListView.query.get(self.cycleId)
        course = CourseListView.query.get(self.courseId)
        concept = ConceptListView.query.get(self.conceptId)
        
        return {
            "id": self.id,
            "cycleId": self.cycleId,
            "cycleName": cycle.name if cycle else "Unknown",
            "courseId": self.courseId,
            "courseName": course.name if course else "Unknown",
            "conceptId": self.conceptId,
            "conceptName": concept.name if concept else "Unknown",
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "isActive": self.isActive
        }

@jwt_required()
def get_costs():
    query = CourseCostModel.query
    
    cycle_id = request.args.get('cycleId')
    course_id = request.args.get('courseId')
    
    if cycle_id:
        query = query.filter_by(cycleId=cycle_id)
    if course_id:
        query = query.filter_by(courseId=course_id)
        
    costs = query.order_by(CourseCostModel.id.desc()).all()
    return jsonify([c.to_dict() for c in costs]), 200

@jwt_required()
def get_cost(id):
    cost = CourseCostModel.query.get(id)
    if not cost:
        return jsonify({'message': 'Costo no encontrado'}), 404
    return jsonify(cost.to_dict()), 200

@jwt_required()
def create_cost():
    data = request.json
    try:
        new_cost = CourseCostModel(
            cycleId=data.get('cycleId'),
            courseId=data.get('courseId'),
            conceptId=data.get('conceptId'),
            amount=data.get('amount'),
            isActive=data.get('isActive', True)
        )
        db.session.add(new_cost)
        db.session.commit()
        return jsonify(new_cost.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_cost(id):
    data = request.json
    try:
        cost = CourseCostModel.query.get(id)
        if not cost:
            return jsonify({'message': 'Costo no encontrado'}), 404
            
        cost.cycleId = data.get('cycleId', cost.cycleId)
        cost.courseId = data.get('courseId', cost.courseId)
        cost.conceptId = data.get('conceptId', cost.conceptId)
        cost.amount = data.get('amount', cost.amount)
        cost.isActive = data.get('isActive', cost.isActive)
        
        db.session.commit()
        return jsonify(cost.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_cost(id):
    try:
        cost = CourseCostModel.query.get(id)
        if not cost:
            return jsonify({'message': 'Costo no encontrado'}), 404
        db.session.delete(cost)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# Boxes Logic
# ---------------------------------------------------------------------------

from app.models.master_scheme.user_model import Users

class BoxModel(db.Model):
    __tablename__ = 'tcajas'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idcaja", Integer, primary_key=True)
    name = db.Column("scaja", String)
    userId = db.Column("idusuario", Integer)
    isActive = db.Column("bactivo", Boolean, default=True)

    def to_dict(self):
        user = Users.query.get(self.userId) if self.userId else None
        return {
            "id": self.id,
            "name": self.name,
            "userId": self.userId,
            "userName": f"{user.firstName} {user.lastName}" if user else None,
            "isActive": self.isActive
        }

@jwt_required()
def get_boxes():
    boxes = BoxModel.query.order_by(BoxModel.id).all()
    return jsonify([b.to_dict() for b in boxes]), 200

@jwt_required()
def get_box(id):
    box = BoxModel.query.get(id)
    if not box:
        return jsonify({'message': 'Caja no encontrada'}), 404
    return jsonify(box.to_dict()), 200

@jwt_required()
def create_box():
    data = request.json
    try:
        new_box = BoxModel(
            name=data.get('name'),
            userId=data.get('userId'),
            isActive=data.get('isActive', True)
        )
        db.session.add(new_box)
        db.session.commit()
        return jsonify(new_box.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_box(id):
    data = request.json
    try:
        box = BoxModel.query.get(id)
        if not box:
            return jsonify({'message': 'Caja no encontrada'}), 404
            
        box.name = data.get('name', box.name)
        box.userId = data.get('userId', box.userId)
        box.isActive = data.get('isActive', box.isActive)
        
        db.session.commit()
        return jsonify(box.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_box(id):
    try:
        box = BoxModel.query.get(id)
        if not box:
            return jsonify({'message': 'Caja no encontrada'}), 404
        db.session.delete(box)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# NCF Logic
# ---------------------------------------------------------------------------

class ClientNCFModel(db.Model):
    __tablename__ = 'tncf'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idsecuencia", Integer, primary_key=True)
    type_ncf = db.Column("stiponcf", String(3))
    prefix = db.Column("sprefijo", String(1), default='B')
    current_number = db.Column("inumeroactual", Integer, default=0)
    max_number = db.Column("inumeromaximo", Integer)
    is_active = db.Column("bactivo", Boolean, default=True)
    expiration_date = db.Column("dfechavencimiento", Date)

    def to_dict(self):
        return {
            "id": self.id,
            "type_ncf": self.type_ncf,
            "prefix": self.prefix,
            "current_number": self.current_number,
            "max_number": self.max_number,
            "is_active": self.is_active,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None
        }

@jwt_required()
def get_ncf_sequences():
    sequences = ClientNCFModel.query.order_by(ClientNCFModel.type_ncf).all()
    return jsonify([s.to_dict() for s in sequences]), 200

@jwt_required()
def get_ncf_sequence(id):
    seq = ClientNCFModel.query.get(id)
    if not seq:
        return jsonify({'message': 'Secuencia no encontrada'}), 404
    return jsonify(seq.to_dict()), 200

@jwt_required()
def create_ncf_sequence():
    data = request.json
    try:
        new_seq = ClientNCFModel(
            type_ncf=data.get('type_ncf'),
            prefix=data.get('prefix'),
            current_number=data.get('current_number'),
            max_number=data.get('max_number'),
            expiration_date=data.get('expiration_date'),
            is_active=data.get('is_active', True)
        )
        db.session.add(new_seq)
        db.session.commit()
        return jsonify(new_seq.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_ncf_sequence(id):
    data = request.json
    try:
        seq = ClientNCFModel.query.get(id)
        if not seq:
            return jsonify({'message': 'Secuencia no encontrada'}), 404
            
        seq.type_ncf = data.get('type_ncf', seq.type_ncf)
        seq.prefix = data.get('prefix', seq.prefix)
        seq.current_number = data.get('current_number', seq.current_number)
        seq.max_number = data.get('max_number', seq.max_number)
        seq.expiration_date = data.get('expiration_date', seq.expiration_date)
        seq.is_active = data.get('is_active', seq.is_active)
        
        db.session.commit()
        return jsonify(seq.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_ncf_sequence(id):
    try:
        seq = ClientNCFModel.query.get(id)
        if not seq:
            return jsonify({'message': 'Secuencia no encontrada'}), 404
        db.session.delete(seq)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# ---------------------------------------------------------------------------
# Taxes Logic
# ---------------------------------------------------------------------------

class ClientTaxModel(db.Model):
    __tablename__ = 'timpuestos'
    __table_args__ = {'schema': 'cliente'}
    
    id = db.Column("idimpuesto", Integer, primary_key=True)
    date = db.Column("dfecha", Date)
    percentage = db.Column("nporciento", db.Numeric)
    isActive = db.Column("bactivo", Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "percentage": float(self.percentage) if self.percentage is not None else 0.0,
            "isActive": self.isActive
        }

@jwt_required()
def get_taxes():
    taxes = ClientTaxModel.query.order_by(ClientTaxModel.date.desc()).all()
    return jsonify([t.to_dict() for t in taxes]), 200

@jwt_required()
def get_tax(id):
    tax = ClientTaxModel.query.get(id)
    if not tax:
        return jsonify({'message': 'Impuesto no encontrado'}), 404
    return jsonify(tax.to_dict()), 200

@jwt_required()
def create_tax():
    data = request.json
    try:
        # If setting active, potentially deactivate others? Or allow multiple?
        # Typically only one general tax is active at a time, but lets keep it flexible or follow business rule.
        # Assuming only one active for now for "Current Tax" view consistency.
        if data.get('isActive'):
            ClientTaxModel.query.filter_by(isActive=True).update({'isActive': False})
            
        new_tax = ClientTaxModel(
            date=data.get('date'),
            percentage=data.get('percentage'),
            isActive=data.get('isActive', True)
        )
        db.session.add(new_tax)
        db.session.commit()
        return jsonify(new_tax.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def update_tax(id):
    data = request.json
    try:
        tax = ClientTaxModel.query.get(id)
        if not tax:
            return jsonify({'message': 'Impuesto no encontrado'}), 404
            
        if data.get('isActive') and not tax.isActive:
             ClientTaxModel.query.filter(ClientTaxModel.id != id).update({'isActive': False})
            
        tax.date = data.get('date', tax.date)
        tax.percentage = data.get('percentage', tax.percentage)
        tax.isActive = data.get('isActive', tax.isActive)
        
        db.session.commit()
        return jsonify(tax.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@jwt_required()
def delete_tax(id):
    try:
        tax = ClientTaxModel.query.get(id)
        if not tax:
            return jsonify({'message': 'Impuesto no encontrado'}), 404
        db.session.delete(tax)
        db.session.commit()
        return jsonify({'message': 'Eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
