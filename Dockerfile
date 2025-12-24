# 1. Usar una imagen ligera de Python
FROM python:3.12-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requisitos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código del proyecto
COPY . .

# 5. Exponer el puerto que usará Flask (Cloud Run usa el 8080 por defecto)
EXPOSE 8080

# 6. Comando para ejecutar la app usando Gunicorn (recomendado para producción)
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "run:app"]