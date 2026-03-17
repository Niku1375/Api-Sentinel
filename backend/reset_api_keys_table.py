from sqlalchemy import text
from app.database.session import engine
from app.database.base import Base
from app.models import api_key  # registers model with Base

def reset_api_keys_table():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS api_keys CASCADE"))
        conn.commit()
        print("Dropped api_keys table")

    Base.metadata.create_all(bind=engine)
    print("Recreated api_keys table with new schema")

if __name__ == "__main__":
    reset_api_keys_table()