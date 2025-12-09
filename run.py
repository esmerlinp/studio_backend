from flask import Flask, request, jsonify
from app.blueprints.usuarios import usuarios_bp
from app.blueprints.auth import auth_bp
from app.security import token_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta
app = Flask(__name__)

# Clave secreta para firmar los tokens
app.config["JWT_SECRET_KEY"] = "super-secret-key-123"  # cámbiala por una segura
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)     # token corto
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)    # token largo

jwt = JWTManager(app)

app.register_blueprint(usuarios_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def hola_mundo():
    return '¡Hola desde Flask!'


#Consumir rutas protegidas con el JWT
#El cliente debe enviar el token en el header: Authorization: Bearer <token>
@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = get_jwt_identity()  # devuelve lo que enviaste como identity
    return jsonify(user)


@app.route('/usuario/<nombre>')
#@token_required
def mostrar_usuario(nombre):
    return f'Hola {nombre} desde Flask!'



@app.route('/buscar')
def buscar():
    #Visita /buscar?q=flask
    query = request.args.get('q', 'nada')
    return f'Buscando: {query}'




if __name__ == '__main__':
    app.run(debug=True)
