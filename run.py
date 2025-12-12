from flask import Flask, request, jsonify
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.auth import auth_bp
from app.blueprints.clientes import clientes_bp
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta
from app.middlewares.track_activity import track_activity
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

# Clave secreta para firmar los tokens
app.config["JWT_SECRET_KEY"] = "super-secret-key-123"  # cámbiala por una segura
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)     # token corto
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)    # token largo

jwt = JWTManager(app)

app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(clientes_bp)


@app.route('/')
def hola_mundo():
    return '¡Hola desde Flask!'


@app.route('/ip')
def get_ip():
    return f'Tu IP es: {request.remote_addr}'




if __name__ == '__main__':
    app.run(debug=True)
