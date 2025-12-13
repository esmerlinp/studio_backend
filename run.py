from flask import Flask, request
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.api.v1.users.routes import users_bp
from app.api.v1.auth.routes import auth_bp
from app.api.v1.clients.routes import client_bp


app = Flask(__name__)

load_dotenv()

# Clave secreta para firmar los tokens
app.config["JWT_SECRET_KEY"] = "super-secret-key-123"  # cámbiala por una segura
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)     # token corto
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)    # token largo

jwt = JWTManager(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)


@app.route('/')
def hola_mundo():
    return '¡Hola desde Flask!'


@app.route('/ip')
def get_ip():
    return f'Tu IP es: {request.remote_addr}'




if __name__ == '__main__':
    app.run(debug=True)
