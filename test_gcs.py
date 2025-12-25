import os
from google.cloud import storage

# 1. Configura la ruta a tu JSON manualmente para esta prueba
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './app/akadmia-1b52b58e2bdd.json'

def test_connection():
    try:
        client = storage.Client()
        # Intentar listar los buckets del proyecto
        buckets = list(client.list_buckets())
        print("✅ Conexión exitosa. Buckets encontrados:")
        for b in buckets:
            print(f" - {b.name}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()