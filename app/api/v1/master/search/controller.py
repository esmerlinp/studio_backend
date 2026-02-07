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
            "redirect_url": f"/dashboard/clients?id={c.clientId}" # Or specific detail page if exists
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
            "redirect_url": f"/dashboard/plans?id={p.id}"
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
            "redirect_url": f"/dashboard/users?id={u.userId}"
        })

    # Search Medical Institutions
    med_inst = MedicalInstitution.query.filter(
        MedicalInstitution.name.ilike(f'%{query}%')
    ).limit(5).all()
    for m in med_inst:
        results.append({
            "label": m.name,
            "category": "Inst. Médicas",
            "redirect_url": f"/dashboard/medical-institutions?id={m.id}"
        })

    return jsonify(results)
