from typing import List, Optional
from app import db
from app.models.master_scheme.plans_model import Plan


def create_plan(
    *,
    code: str,
    name: str,
    description: Optional[str] = None,
    max_users: Optional[int] = None,
    max_storage_gb: Optional[int] = None,
    support_level: Optional[str] = None,
    environment_type: Optional[str] = None,
) -> Plan:

    # Validar código único
    if Plan.query.filter_by(code=code).first():
        raise ValueError("Plan code already exists")

    plan = Plan(
        code=code,
        name=name,
        description=description,
        max_users=max_users,
        max_storage_gb=max_storage_gb,
        support_level=support_level,
        environment_type=environment_type,
        is_active=True
    )

    try:
        db.session.add(plan)
        db.session.commit()
        return plan
    except Exception:
        db.session.rollback()
        raise



def get_plans(active_only: bool = True) -> List[Plan]:
    query = Plan.query

    if active_only:
        query = query.filter_by(is_active=True)
    
    return query.order_by(Plan.created_at.desc()).all()


def get_plan_by_id(plan_id: int) -> Optional[Plan]:
    return Plan.query.get(plan_id)


def update_plan(
    plan_id: int,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    max_users: Optional[int] = None,
    max_storage_gb: Optional[int] = None,
    support_level: Optional[str] = None,
    environment_type: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> Optional[Plan]:

    plan = Plan.query.get(plan_id)
    if not plan:
        return None

    if name is not None:
        plan.name = name
    if description is not None:
        plan.description = description
    if max_users is not None:
        plan.max_users = max_users
    if max_storage_gb is not None:
        plan.max_storage_gb = max_storage_gb
    if support_level is not None:
        plan.support_level = support_level
    if environment_type is not None:
        plan.environment_type = environment_type
    if is_active is not None:
        plan.is_active = is_active

    try:
        db.session.commit()
        return plan
    except Exception:
        db.session.rollback()
        raise



def deactivate_plan(plan_id: int) -> bool:
    plan = Plan.query.get(plan_id)
    if not plan:
        return False

    plan.is_active = False

    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise


def delete_plan(plan_id: int) -> bool:
    plan = Plan.query.get(plan_id)
    if not plan:
        return False

    try:
        db.session.delete(plan)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
