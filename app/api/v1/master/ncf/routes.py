from flask import Blueprint
from .controller import get_sequences, create_sequence, toggle_sequence, get_logs

ncf_bp = Blueprint("ncf", __name__)

ncf_bp.get("/")(get_sequences)
ncf_bp.post("/")(create_sequence)
ncf_bp.patch("/<int:sequence_id>")(toggle_sequence)
ncf_bp.get("/logs")(get_logs)
