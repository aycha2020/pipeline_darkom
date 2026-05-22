 # Database configuration for PostgreSQL connection using SQLAlchemy


from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASSWORD = "Aishahbb2021"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "darkom_dwh"

DATABASE_URL = (
    f"postgresql://{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# test connection  de la base de données
try:
    conn = engine.connect()
    print(" PostgreSQL connected")
    conn.close()

except Exception as e:
    print(" Connection failed")
    print(e)