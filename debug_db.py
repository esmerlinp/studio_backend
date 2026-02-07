
import os
from app import create_app
from app.extensions import db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    schemas = inspector.get_schema_names()
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        for table in tables:
            if "dbauditoria" in table.lower():
                print(f"Found table: {schema}.{table}")
