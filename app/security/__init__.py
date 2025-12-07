from functools import wraps
from flask import request, abort

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, description="Token requerido")
        
        if not token.startswith('Bearer '):
            abort(401, description="Formato inválido. Use Bearer <token>")
        
        token = token.split(' ')[1]  # Extrae token puro
        # Aquí validas contra DB o JWT
        if token != 'token_valido_ejemplo':  # Reemplaza con tu lógica
            abort(401, description="Token inválido")
        
        return f(*args, **kwargs)
    return decorated