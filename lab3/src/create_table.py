from sqlalchemy import text
from models import Base
from db_config import *

def create_db():
    Base.metadata.create_all(engine)

    with engine.connect() as conn:
        for table_name in Base.metadata.tables.keys():
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
            count = result.scalar()
            print(f"таблица '{table_name}' создана ({count} строк)")

if __name__ == "__main__":
    create_db()
