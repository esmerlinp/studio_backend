from google import genai
from google.genai import types
import os
from .chatbot_tools import TOOLS_MAP
from dotenv import load_dotenv
from flask import current_app

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Inicializamos el cliente de la nueva SDK
client = genai.Client(api_key=api_key)

def process_chat_message(user_message: str, history: list = None, context: dict = None):
    """
    Procesa un mensaje del usuario utilizando la nueva SDK de Google GenAI.
    Maneja el historial, ejecuta herramientas automáticamente y utiliza el contexto de la página.
    """
    if history is None:
        history = []

    # 1. Preparar historial para la nueva SDK
    # La nueva SDK espera objetos de tipo Content o diccionarios con 'role' y 'parts'
    contents = []
    for msg in history:
        role = 'user' if msg.get('role') == 'user' else 'model'
        content = msg.get('content', '')
        contents.append(types.Content(role=role, parts=[types.Part(text=content)]))

    # 2. Configurar herramientas
    # En la nueva SDK podemos pasar las funciones directamente en una lista de herramientas
    tools_list = [types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name=name,
            description=func.__doc__.strip() if func.__doc__ else name,
            parameters=types.Schema(
                type='OBJECT',
                properties={
                    # Aquí la nueva SDK suele inferir parámetros si se decoran o se pasan bien,
                    # pero para asegurar, podemos ser explícitos o usar la inferencia simple.
                    # Dado que nuestras funciones en TOOLS_MAP son simples, la SDK suele manejarlas.
                }
            )
        ) for name, func in TOOLS_MAP.items()
    ])]
    
    # Simplificación: En la nueva SDK 1.x, podemos pasar las funciones de Python directamente 
    # y el cliente se encarga de la introspección.
    auto_tools = list(TOOLS_MAP.values())

    try:
        # 3. Construir el mensaje con contexto si existe
        if context:
            prompt = f"""
[CONTEXTO DE LA PANTALLA ACTUAL]
El usuario está viendo la siguiente página en el dashboard administrativo:
- Título: {context.get('title', 'N/A')}
- URL: {context.get('url', 'N/A')}

Contenido de texto visible:
{context.get('content', '')[:3000]}

Datos de formularios detectados:
{context.get('formData', {})}

[INSTRUCCIÓN DEL SISTEMA]
Actúas como un Asistente Global del Sistema "Akdmia".
TIENES ACCESO A TODA LA BASE DE DATOS del sistema a través de tus herramientas (Usuarios, Roles, Pantallas, Clientes, Pagos, etc.).
- Si el usuario pregunta algo específico de la pantalla actual (ej: "este cliente", "este formulario"), USA EL CONTEXTO DE PANTALLA.
- Si el usuario pregunta algo general o busca datos no visibles (ej: "¿Quién es el usuario X?", "Busca la pantalla Y"), USA TUS HERRAMIENTAS GLOBALES.
- NO te limites al contexto de la pantalla si la respuesta requiere buscar en la base de datos global.
[FIN INSTRUCCIÓN]

Consulta del usuario: {user_message}
"""
        else:
            prompt = user_message

        # 4. Enviar mensaje con el chat (maneja historial y herramientas)
        # Usamos generate_content con el historial acumulado (contents) + el nuevo prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents + [types.Content(role='user', parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(
                tools=auto_tools,
                # La nueva SDK maneja el automatic function calling por defecto si pasas herramientas
            )
        )
        
        return response.text
        
    except Exception as e:
        current_app.logger.error(f"Error en Chatbot Service (GenAI SDK): {str(e)}")
        # Loggear el traceback completo para debugging si es necesario
        import traceback
        current_app.logger.error(traceback.format_exc())
        return "Lo siento, hubo un error al procesar tu solicitud con el nuevo motor de IA. Por favor intenta de nuevo."
