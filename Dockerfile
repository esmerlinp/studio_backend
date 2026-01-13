# 1. Usar una imagen ligera de Python
FROM python:3.12-slim

# 2. Instalar dependencias del sistema (gettext para compilar traducciones)
# Se limpia el cache de apt para mantener la imagen ligera
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# 3. Establecer el directorio de trabajo
WORKDIR /app

# 4. Copiar el archivo de requisitos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código del proyecto
COPY . .

# 6. COMPILAR TRADUCCIONES
# Buscamos todos los archivos .po y generamos su .mo automáticamente
# RUN find locales -name "*.po" -exec msgfmt {} -o {} \; && \
#     sed -i 's/\.po/\.mo/g' locales/**/LC_MESSAGES/*.po || true

# RUN msgfmt locales/es/LC_MESSAGES/messages.po -o locales/es/LC_MESSAGES/messages.mo && \
#     msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo
# Nota: Si usas Flask-Babel, es mucho más simple: 
# RUN pybabel compile -d locales

# 7. Exponer el puerto
EXPOSE 8080

# 8. Comando para ejecutar la app
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "run:app"]