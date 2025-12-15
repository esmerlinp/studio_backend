import psycopg2
import psycopg2.extras
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear Pool
db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def get_connection(scheme="public"):
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute(f"SET search_path TO {scheme};")
    return conn



def fetch_data(query, params=None, as_dict=True):
    """
    Retorna múltiples filas.
    
    Example:
    
        clientes = fetch_data("SELECT * FROM clientes WHERE status = %s", ("ACTIVO",))
        print(clientes)
    """
    conn = None
    try:
        conn = get_connection()
        cursor_factory = psycopg2.extras.RealDictCursor if as_dict else None

        with conn.cursor(cursor_factory=cursor_factory) as cur:
            cur.execute(query, params)
            return cur.fetchall()

    except Exception as e:
        print(f"[fetch_data] Error: {e}")
        return []

    finally:
        if conn:
            db_pool.putconn(conn)


def fetch_one(query, params=None, as_dict=True):
    """
    Retorna una sola fila.
    
    Example:
        cliente = fetch_one("SELECT * FROM clientes WHERE client_id = %s", (15,))
        print(cliente)
    """
    conn = None
    try:
        conn = get_connection()
        cursor_factory = psycopg2.extras.RealDictCursor if as_dict else None

        with conn.cursor(cursor_factory=cursor_factory) as cur:
            cur.execute(query, params)
            return cur.fetchone()

    except Exception as e:
        print(f"[fetch_one] Error: {e}")
        return None

    finally:
        if conn:
            db_pool.putconn(conn)


def execute_non_query(query, params=None, return_id=False):
    conn = None
    try:
        conn = get_connection()

        with conn.cursor() as cur:
            cur.execute(query, params)

            if return_id:
                if cur.description:  # ← solo si hay RETURNING
                    row = cur.fetchone()
                    conn.commit()
                    return row[0] if row else None
                else:
                    conn.commit()
                    return None

            conn.commit()
            return cur.rowcount

    except Exception as e:
        print(f"[execute_non_query] Error: {e}")
        if conn:
            conn.rollback()
        return None if return_id else 0

    finally:
        if conn:
            db_pool.putconn(conn)





