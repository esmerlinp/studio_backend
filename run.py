from flask import Flask, request
from app.blueprints.usuarios import usuarios_bp
from app.security import token_required

app = Flask(__name__)
app.register_blueprint(usuarios_bp)


@app.route('/')
def hola_mundo():
    return '¡Hola desde Flask!'


@app.route('/usuario/<nombre>')
@token_required
def mostrar_usuario(nombre):
    return f'Hola {nombre} desde Flask!'



@app.route('/buscar')
def buscar():
    #Visita /buscar?q=flask
    query = request.args.get('q', 'nada')
    return f'Buscando: {query}'


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    return f'Bienvenido {usuario}'

if __name__ == '__main__':
    app.run(debug=True)