from sqlalchemy import inspect, text, MetaData
from tabulate import tabulate
from models import *
from db_config import *

metadata = MetaData() 

def show_table(table_name, limit=None):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    table_name = table_name.lower()

    if table_name not in tables:
        print(f"таблица '{table_name}' не найдена")
        return
    
    sql = f"SELECT * FROM {table_name}"
    if limit is not None:
        sql += f" LIMIT {limit}"

    query = text(sql)
    result = session.execute(query).fetchall()
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    print(f"таблица: {table_name}")
    print(tabulate(result, headers=columns, tablefmt="fancy_grid", disable_numparse=True))
    

def show_all_table(limit=None):
    show_table("cinema", limit)
    show_table("films", limit)
    show_table("festival", limit)
    show_table("cinema_halls", limit)
    show_table("sessions", limit)
    show_table("tickets", limit)
    show_table("prizes", limit)
