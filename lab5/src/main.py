from create_table import *
from insert_data import *
from questions import *
from show_table import *
from delete_table import *
from generate_data import *
from measure_time import *

def main():
    # # # удаляем таблицы 
    # delete_all_tables()

    # # cоздаём таблицы
    # create_db()

    # # генерируем данные
    # generate_database()
    
    # # показываем таблицы 
    # show_all_table(10)

    # # замеряем время всех запросов
    # measure_all()
    ticket_prices("Прошептать", 1, True, True)
    
if __name__ == "__main__":
    main()
