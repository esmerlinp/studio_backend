from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Configuración del Limiter
# Instancia global del limitador
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://", # En producción usa Redis
    strategy="fixed-window" # O "moving-window"
)