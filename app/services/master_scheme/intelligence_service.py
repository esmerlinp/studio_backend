from google import genai
import os
from dotenv import load_dotenv
# Configura tu llave de API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def ai_generic_generator(template, data_dict, model="gemini-2.0-flash"):
    """
    Servicio genérico que inyecta datos en una plantilla y consulta a Gemini.
    """
    try:
        # Llenamos la plantilla con los datos dinámicos
        full_prompt = template.format(**data_dict)

        response = client.models.generate_content(
            model=model,
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error en IA Service: {str(e)}")
    
