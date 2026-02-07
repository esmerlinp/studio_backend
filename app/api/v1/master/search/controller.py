from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.master_scheme.client_model import Client
from app.models.master_scheme.plans_model import Plan
from app.models.master_scheme.user_model import User
from app.models.master_scheme.medical_institution_model import MedicalInstitution
from sqlalchemy import or_

search_bp = Blueprint('search', __name__, url_prefix='/api/v1/master/search')

@search_bp.route('/', methods=['GET'])
@jwt_required()
def global_search():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify([])

    results = []

    # Search Clients
    clients = Client.query.filter(or_(
        Client.name.ilike(f'%{query}%'),
        Client.businessName.ilike(f'%{query}%'),
        Client.documentNumber.ilike(f'%{query}%')
    )).limit(5).all()
    for c in clients:
        results.append({
            "label": c.name,
            "category": "Clientes",
            "redirect_url": f"/dashboard/clients/{c.clientId}"
        })

    # Search Plans
    plans = Plan.query.filter(or_(
        Plan.name.ilike(f'%{query}%'),
        Plan.code.ilike(f'%{query}%')
    )).limit(5).all()
    for p in plans:
        results.append({
            "label": p.name,
            "category": "Planes",
            "redirect_url": f"/dashboard/plans?id={p.id}"  # Plans doesn't seem to have a detail page in run.py yet, keeping as query or maybe just list? 
            # Looking at run.py: dashboard_plans just lists. There is no detail route for plans yet in the provided run.py snippet.
            # However, the user asked to fix "client detail redirect".
            # unique detail page for clients is /dashboard/clients/<int:clientId>
            # For others, if they don't have a detail page, maybe they just go to list? 
            # Users has /dashboard/users?id=... logic in run.py (lines 526-529).
            # Medical Institutions has /dashboard/medical-institutions but no detail route seen.
            # I will fix Client specifically as requested. 
            # For Users, run.py has specific logic to filter by ID if provided, so ?id= is actually correct there!
            # For Plans, there is no ID filter in run.py dashboard_plans.
            # For Medical Institutions, no ID filter either.
            
            # Re-reading user request: "al ir a un detalle de un cliente especifico me redirecciona a la lista... ?id=76"
            # So Client is the main one broken because it DOES have a detail route.
            # Users ?id= works because dashboard_users handles it.
            # I will Fix Client. I will leave others as is or adjust if I see they support it.
        })
    
    # Search Plans
    plans = Plan.query.filter(or_(
        Plan.name.ilike(f'%{query}%'),
        Plan.code.ilike(f'%{query}%')
    )).limit(5).all()
    for p in plans:
        results.append({
            "label": p.name,
            "category": "Planes",
            "redirect_url": f"/dashboard/plans?search={p.name}" # Better to search by name if no detail page
        })

    # Search Users
    users = User.query.filter(or_(
        User.username.ilike(f'%{query}%'),
        User.firstName.ilike(f'%{query}%'),
        User.lastName.ilike(f'%{query}%'),
        User.email.ilike(f'%{query}%')
    )).limit(5).all()
    for u in users:
        results.append({
            "label": f"{u.firstName} {u.lastName} ({u.username})",
            "category": "Usuarios",
            "redirect_url": f"/dashboard/users?id={u.userId}" # This one is supported in run.py
        })

    # Search Medical Institutions
    med_inst = MedicalInstitution.query.filter(
        MedicalInstitution.name.ilike(f'%{query}%')
    ).limit(5).all()
    for m in med_inst:
        results.append({
            "label": m.name,
            "category": "Inst. Médicas",
            "redirect_url": f"/dashboard/medical-institutions?search={m.name}"
        })

    return jsonify(results)
