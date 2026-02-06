from app import db
from app.models.master_scheme.ncf_model import NCFLog
from ..utils.ecf.xml_builder import ECFBuilder
from ..utils.ecf.signer import ECFSigner
from ..utils.ecf.dgii_client import DGIIClient
import os

class ECFService:
    @staticmethod
    def process_electronic_invoice(invoice_data, client_id, stripe_invoice_id, ncf):
        """
        Main method to handle the complete e-CF flow.
        """
        try:
            # 1. Build XML
            builder = ECFBuilder(invoice_data)
            xml_raw = builder.get_xml_string()

            # 2. Sign XML
            # In a real scenario, paths and passwords would come from secure config/env
            p12_path = os.getenv("DGII_P12_PATH")
            p12_pass = os.getenv("DGII_P12_PASSWORD")
            
            if p12_path and p12_pass:
                signer = ECFSigner(p12_path, p12_pass)
                xml_signed = signer.sign_xml(xml_raw)
            else:
                # Fallback for dev/missing config
                xml_signed = xml_raw
                print("Warning: XML not signed. DGII_P12_PATH or DGII_P12_PASSWORD not set.")

            # 3. Send to DGII
            # Note: DGII environment (test/prod) should be configurable
            client = DGIIClient(environment=os.getenv("DGII_ENVIRONMENT", "test"))
            # client.get_token(os.getenv("DGII_CERT_ID"), os.getenv("DGII_P12_PASSWORD"))
            
            result = client.send_ecf(xml_signed)
            track_id = result.get("trackId")
            status = result.get("status", "PENDIENTE")

            # 4. Create/Update NCF Log with e-CF info
            # We assume the NCF was already reserved by NCFService
            log_entry = NCFLog.query.filter_by(ncf_assigned=ncf, stripe_invoice_id=stripe_invoice_id).first()
            
            if not log_entry:
                log_entry = NCFLog(
                    client_id=client_id,
                    ncf_assigned=ncf,
                    stripe_invoice_id=stripe_invoice_id
                )
                db.session.add(log_entry)

            log_entry.track_id = track_id
            log_entry.ecf_status = status
            # log_entry.xml_url = ... (logic to save to GCS or S3)
            
            db.session.commit()
            
            return {
                "ncf": ncf,
                "track_id": track_id,
                "status": status
            }

        except Exception as e:
            db.session.rollback()
            print(f"Error processing e-CF: {str(e)}")
            raise e
