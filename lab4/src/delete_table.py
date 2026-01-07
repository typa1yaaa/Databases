from sqlalchemy import inspect, text, MetaData
from db_config import *

metadata = MetaData() 

def delete_table(table_name):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    table_name = table_name.lower()

    if table_name not in tables:
        print(f"таблица '{table_name}' не найдена")
        return

    try:
        session.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
        session.commit()
        print(f"таблица '{table_name}' успешно удалена")
    except Exception as e:
        session.rollback()
        print(f"ошибка при удалении таблицы '{table_name}': {e}")

def delete_all_tables():
    # порядок важен, чтобы сначала удалить зависимые таблицы
    tables = [
        "tickets",
        "sessions",
        "cinema_halls",
        "prizes",
        "festival",
        "films",
        "cinema"
    ]

    for t in tables:
        delete_table(t)