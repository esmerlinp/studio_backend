
from uuid import UUID
from app import db
from app.models.master_scheme.user_client_model import UsuarioCliente
from app.models.master_scheme.client_model import Client
from sqlalchemy.exc import IntegrityError
from typing import List


def assign_user_to_client_onboard(*, user_id: int, client_uuid: str) -> UsuarioCliente:
    relation = UsuarioCliente(
        user_id=user_id,
        client_uuid=client_uuid
    )
    db.session.add(relation)
    return relation


def assign_user_to_client(
    *,
    user_id: int,
    client_uuid: str,
    commit: bool = True
) -> UsuarioCliente:

    relation = UsuarioCliente(
        user_id=user_id,
        client_uuid=client_uuid
    )

    try:
        db.session.add(relation)
        if commit:
            db.session.commit()
        else:
            db.session.flush()

        return relation

    except Exception as e:
        if commit:
            db.session.rollback()
        raise  e



# def get_client_by_userId(user_id: int) -> Client:
#     cliente = UsuarioCliente.query.filter_by(user_id=user_id).first()
#     return get_client_by_id(client_id=cliente.clientId)



def get_clients_by_user(user_id: int) -> list[UsuarioCliente]:
    """
    Retorna todos los clientes a los que el usuario tiene acceso.
    """
    
    return UsuarioCliente.query.filter_by(user_id=user_id).all()

def get_client_by_user(user_id: int) -> Client:
    """
    Retorna el cliente del usuario.
    """
    relacion = UsuarioCliente.query.filter_by(user_id=user_id).first()
    cliente = Client.query.filter_by(uuid=relacion.client_uuid).first()
    return cliente


def get_users_by_client(client_uuid: UUID) -> List[UsuarioCliente]:
    """
    Retorna todos los usuarios asociados a un cliente.
    """
    return UsuarioCliente.query.filter_by(client_uuid=client_uuid).all()



def user_has_access_to_client(
    *,
    user_id: int,
    client_uuid: UUID
) -> bool:
    """
    Verifica si un usuario tiene acceso a un cliente.
    """
    return (
        UsuarioCliente.query
        .filter_by(user_id=user_id, client_uuid=client_uuid)
        .first()
        is not None
    )



def remove_user_from_client(
    *,
    user_id: int,
    client_uuid: UUID
) -> bool:
    """
    Elimina la relación entre usuario y cliente.
    """
    relation = UsuarioCliente.query.filter_by(
        user_id=user_id,
        client_uuid=client_uuid
    ).first()

    if not relation:
        return False

    db.session.delete(relation)
    db.session.commit()
    return True
