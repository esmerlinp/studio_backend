from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class CafeteriaProduct(db.Model):
    __tablename__ = "cafeteria_reservada_productos"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idproducto", db.Integer, primary_key=True)
    name = db.Column("snombre", db.String(100), nullable=False)
    description = db.Column("sdescripcion", db.String(255), nullable=True)
    price = db.Column("nprecio", db.Numeric(10, 2), nullable=False)
    cost = db.Column("ncosto", db.Numeric(10, 2), nullable=True)
    stock = db.Column("icantidad", db.Integer, default=0)
    category = db.Column("scategoria", db.String(50), nullable=True) # Bebidas, Snacks, Plato Fuerte
    imageUrl = db.Column("surlimagen", db.String(255), nullable=True)
    
    # Allergens stored as a list of allergy IDs or names: [1, 5] or ["Maní", "Gluten"]
    allergens = db.Column("jalergias", JSONB, nullable=True)
    isActive = db.Column("bactivo", db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "category": self.category,
            "imageUrl": self.imageUrl,
            "allergens": self.allergens,
            "isActive": self.isActive
        }

class CafeteriaTransaction(db.Model):
    __tablename__ = "cafeteria_transacciones"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idtransaccion", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    date = db.Column("dfecha", db.DateTime, default=datetime.utcnow, nullable=False)
    totalAmount = db.Column("ntotal", db.Numeric(10, 2), nullable=False)
    paymentMethod = db.Column("smetodopago", db.String(20), nullable=False) # 'credit', 'cash', 'card', 'balance'
    status = db.Column("sestado", db.String(20), default='completed') # completed, pending, cancelled
    
    # Relationship to items
    items = db.relationship('CafeteriaTransactionItem', backref='transaction', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "date": self.date.isoformat(),
            "totalAmount": float(self.totalAmount),
            "paymentMethod": self.paymentMethod,
            "status": self.status,
            "items": [item.to_dict() for item in self.items]
        }

class CafeteriaTransactionItem(db.Model):
    __tablename__ = "cafeteria_transacciones_detalles"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("iddetalle", db.Integer, primary_key=True)
    transactionId = db.Column("idtransaccion", db.Integer, db.ForeignKey(CafeteriaTransaction.id), nullable=False)
    productId = db.Column("idproducto", db.Integer, db.ForeignKey(CafeteriaProduct.id), nullable=False)
    quantity = db.Column("icantidad", db.Integer, nullable=False)
    unitPrice = db.Column("nprecionunitario", db.Numeric(10, 2), nullable=False)
    subtotal = db.Column("nsubtotal", db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "productId": self.productId,
            "quantity": self.quantity,
            "unitPrice": float(self.unitPrice),
            "subtotal": float(self.subtotal)
        }

class StudentDietaryRestriction(db.Model):
    __tablename__ = "estudiantes_restricciones"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idrestriccion", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False)
    
    # Categories the parent explicitely blocked: ["Sodas", "Candy"]
    restrictedCategories = db.Column("jcategoriasrest", JSONB, nullable=True)
    
    # Specific items blocked by ID: [101, 205]
    restrictedItems = db.Column("jitemsrest", JSONB, nullable=True)

    # Daily spending limit (0 = no limit)
    dailyLimit = db.Column("nlimitediario", db.Numeric(10, 2), default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "restrictedCategories": self.restrictedCategories,
            "restrictedItems": self.restrictedItems,
            "dailyLimit": float(self.dailyLimit)
        }

class StudentWallet(db.Model):
    __tablename__ = "estudiantes_billetera"
    __table_args__ = {"schema": "cliente"}

    id = db.Column("idbilletera", db.Integer, primary_key=True)
    studentId = db.Column("idestudiante", db.Integer, db.ForeignKey("cliente.estudiantes.idestudiante"), nullable=False, unique=True)
    balance = db.Column("nsaldo", db.Numeric(10, 2), default=0.00)
    lastUpdated = db.Column("dultimaactualizacion", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isActive = db.Column("bactivo", db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "studentId": self.studentId,
            "balance": float(self.balance),
            "lastUpdated": self.lastUpdated.isoformat(),
            "isActive": self.isActive
        }
