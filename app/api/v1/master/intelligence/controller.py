
from app.utils.responses import success, error
from app.services.master_scheme.intelligence_service import generar_reporte_estudiante
from app import limiter
from flask_jwt_extended import jwt_required
import json

# @limiter.limit("100 per minute")
@jwt_required()
def get_report(student_id):
    
    # Simulación de datos extraídos de tu base de datos Akdmia
    estudiante_ejemplo = {
        "notas": [],
        "comida": "Se salta el desayuno frecuentemente, consume azúcares procesados en el recreo.",
        "tareas": "Entregó tarde el proyecto de Geometría. Excelente redacción en el ensayo de Lenguaje."
    }

    # Ejecución
    reporte = generar_reporte_estudiante(estudiante_ejemplo)
    data_json = json.loads(reporte.replace("```json", "").replace("```", ""))

    return success(data=data_json)