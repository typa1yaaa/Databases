from sqlalchemy import inspect, text, MetaData
from tabulate import tabulate
from models import *
from db_config import *

metadata = MetaData() 

def show_table(table_name):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    table_name = table_name.lower()

    if table_name not in tables:
        print(f"таблица '{table_name}' не найдена")
        return

    query = text(f"SELECT * FROM {table_name}")
    result = session.execute(query).fetchall()
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    print(f"таблица: {table_name}")
    print(tabulate(result, headers=columns, tablefmt="fancy_grid", disable_numparse=True))
    

def show_all_table():
    show_table("cinema")
    show_table("films")
    show_table("festival")
    show_table("cinema_halls")
    show_table("sessions")
    show_table("tickets")
    show_table("prizes")
