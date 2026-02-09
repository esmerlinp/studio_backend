from app import db
from datetime import datetime, date
from app.models.client_scheme.cafeteria_models import (
    CafeteriaProduct, CafeteriaTransaction, CafeteriaTransactionItem, 
    StudentDietaryRestriction, StudentWallet
)
from app.models.client_scheme.student_details_models import StudentAllergy
from app.services.event_bus_service import emit_event, Events

def process_cafeteria_transaction(student_id, cart_items, payment_method='balance'):
    """
    Process a purchase in the cafeteria.
    Includes: Balance check, Daily Limit check, and Allergy check.
    """
    # 1. Fetch Student Config & Wallet
    wallet = StudentWallet.query.filter_by(studentId=student_id).first()
    restriction = StudentDietaryRestriction.query.filter_by(studentId=student_id).first()
    student_allergies = StudentAllergy.query.filter_by(studentId=student_id).all()
    
    # Get allergy IDs the student has
    allergy_ids = [a.allergyId for a in student_allergies]
    
    total_amount = 0
    items_to_create = []
    
    # 2. Check each product
    for item in cart_items:
        product = CafeteriaProduct.query.get(item['productId'])
        if not product or not product.isActive:
            return None, f"Producto {item.get('productId')} no disponible"
            
        # --- ALLERGY GUARD ---
        if product.allergens:
            # product.allergens is a list of IDs or names
            for p_allergy in product.allergens:
                if p_allergy in allergy_ids:
                    return None, f"BLOQUEO DE SALUD: El estudiante es alérgico a {product.name}"

        # --- RESTRICTION GUARD ---
        if restriction:
            if restriction.restrictedItems and product.id in restriction.restrictedItems:
                return None, f"BLOQUEO PARENTAL: Este producto no está permitido para el estudiante"
            
            if restriction.restrictedCategories and product.category in restriction.restrictedCategories:
                return None, f"BLOQUEO PARENTAL: La categoría {product.category} está restringida"

        quantity = item['quantity']
        subtotal = product.price * quantity
        total_amount += subtotal
        
        items_to_create.append(CafeteriaTransactionItem(
            productId=product.id,
            quantity=quantity,
            unitPrice=product.price,
            subtotal=subtotal
        ))

    # 3. FINANCIAL GUARD
    if payment_method == 'balance':
        if not wallet or wallet.balance < total_amount:
            return None, "Saldo insuficiente en la billetera estudiantil"
        
        if restriction and restriction.dailyLimit > 0:
            # Check today's spending
            today_total = db.session.query(db.func.sum(CafeteriaTransaction.totalAmount)).filter(
                CafeteriaTransaction.studentId == student_id,
                db.func.date(CafeteriaTransaction.date) == date.today()
            ).scalar() or 0
            
            if float(today_total) + float(total_amount) > float(restriction.dailyLimit):
                return None, f"Límite de gasto diario excedido (Límite: ${restriction.dailyLimit})"

    # 4. EXECUTE TRANSACTION
    transaction = CafeteriaTransaction(
        studentId=student_id,
        totalAmount=total_amount,
        paymentMethod=payment_method,
        status='completed'
    )
    db.session.add(transaction)
    db.session.flush() # Get transaction.id
    
    for t_item in items_to_create:
        t_item.transactionId = transaction.id
        db.session.add(t_item)
        
    if payment_method == 'balance':
        wallet.balance -= total_amount
        
    db.session.commit()
    
    # 5. Emit Event
    emit_event(Events.STUDENT_CAFETERIA_PURCHASE, {
        "studentId": student_id,
        "amount": float(total_amount),
        "items": [p.productId for p in items_to_create]
    })
    
    return transaction.id, None

def get_student_wallet_info(student_id):
    """Retrieve wallet balance and restrictions."""
    wallet = StudentWallet.query.filter_by(studentId=student_id).first()
    restriction = StudentDietaryRestriction.query.filter_by(studentId=student_id).first()
    
    return {
        "balance": float(wallet.balance) if wallet else 0,
        "restrictions": restriction.to_dict() if restriction else None
    }

def add_funds_to_wallet(student_id, amount):
    """Top up student wallet."""
    wallet = StudentWallet.query.filter_by(studentId=student_id).first()
    if not wallet:
        wallet = StudentWallet(studentId=student_id, balance=0)
        db.session.add(wallet)
        
    wallet.balance += amount
    db.session.commit()
    
    emit_event(Events.STUDENT_WALLET_UPDATE, {
        "studentId": student_id,
        "newBalance": float(wallet.balance)
    })
    return wallet.balance
