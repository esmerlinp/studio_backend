from app import db, audit_log
from app.models.master_scheme.ncf_model import NCFSequence, NCFLog
from datetime import date
from app.utils.types import ResourceTypes, ActionType
from flask import g
from app.utils import i18n  # Importar el módulo de idiomas

class NCFService:
    
    
    @staticmethod
    @audit_log(action=ActionType.CREATE, resource_type=ResourceTypes.NCF)
    def create_sequence(type_ncf, prefix, start_num, max_num, expiration_date:date = None):
        """Registra un nuevo rango autorizado por la DGII."""
        # Opcional: Inhabilitar cualquier secuencia activa del mismo tipo primero
        NCFSequence.query.filter_by(type_ncf=type_ncf, is_active=True).update({"is_active": False})
        
        new_seq = NCFSequence(
            type_ncf=type_ncf,
            prefix=prefix,
            current_number=start_num,
            max_number=max_num,
            is_active=True,
            expiration_date=expiration_date
        )
        db.session.add(new_seq)
        g.audit_new_values = new_seq.to_dict()
        db.session.commit()
        return new_seq
    
    
    
    @staticmethod
    @audit_log(action=ActionType.UPDATE, resource_type=ResourceTypes.NCF)
    def toggle_sequence_status(sequence_id, active=False):
        """Habilita o inhabilita una secuencia por su ID."""
        seq = NCFSequence.query.get(sequence_id)
        g.audit_old_values = seq.to_dict()
        if seq:
            seq.is_active = active
            g.audit_new_values = seq.to_dict()
            db.session.commit()
            return True
        return False
    
    
    
    @staticmethod
    @audit_log(action=ActionType.UPDATE, resource_type=ResourceTypes.NCF)
    def update_sequence_limits(sequence_id, new_max=None, new_current=None, new_expiration_date=None):
        """Modifica los límites o el contador actual de una secuencia."""
        seq = NCFSequence.query.get(sequence_id)
        if not seq: return False
        g.audit_old_values = seq.to_dict()
        if new_max: seq.max_number = new_max
        if new_current: seq.current_number = new_current
        if new_expiration_date: seq.expiration_date = new_expiration_date
        g.audit_new_values = seq.to_dict()
        db.session.commit()
        return True
    
    
    
    @staticmethod
    @audit_log(action=ActionType.CREATE, resource_type=ResourceTypes.NCF_LOG)
    def generate_and_assign_ncf(client_id: int, type_ncf: str, stripe_invoice_id: str = None):
        """
        Obtiene el siguiente NCF, incrementa la secuencia y lo registra en el log.
        """
        try:
            # 1. Bloqueamos la fila de la secuencia para que nadie más la lea hasta que terminemos
            sequence = NCFSequence.query.filter_by(
                type_ncf=type_ncf, 
                is_active=True
            ).with_for_update().first()

            if not sequence:
                raise Exception(i18n._("error.ncf.no_active_sequence") % type_ncf)

            if sequence.current_number > sequence.max_number:
                raise Exception(i18n._("error.ncf.exhausted") % type_ncf)

            if sequence.expiration_date and sequence.expiration_date < date.today():
                sequence.is_active = False # La auto-inhabilitamos
                db.session.commit()
                msg = i18n._("error.ncf.expired") % {
                                    'type': type_ncf, 
                                    'date': sequence.expiration_date
                                }
                raise Exception(msg)
                        
            
            # 2. Generar el string formateado
            ncf_string = sequence.get_next_ncf()

            # 3. Incrementar el contador
            sequence.current_number += 1

            # 4. Registrar en el log de auditoría de NCF
            new_log = NCFLog(
                client_id=client_id,
                ncf_assigned=ncf_string,
                stripe_invoice_id=stripe_invoice_id
            )
            g.audit_new_values = new_log.to_dict()
            db.session.add(new_log)
            
            # Guardamos cambios (esto libera el bloqueo de la fila)
            db.session.commit()
            
            return ncf_string

        except Exception as e:
            db.session.rollback()
            print(f"Error en NCFService: {str(e)}")
            raise e

    @staticmethod
    @audit_log(action=ActionType.READ, resource_type=ResourceTypes.NCF, resource_id_arg="type_ncf")
    def get_remaining_count(type_ncf: str):
        """Devuelve cuántos números quedan antes de que se agote la secuencia."""
        seq = NCFSequence.query.filter_by(type_ncf=type_ncf, is_active=True).first()
        if seq:
            return seq.max_number - seq.current_number + 1
        return 0