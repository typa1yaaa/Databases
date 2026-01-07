from create_table import *
from insert_data import *
from questions import *
from show_table import *
from delete_table import *
from generate_data import *
from measure_time import *

def main():
    # # удаляем таблицы 
    # delete_all_tables()

    # # cоздаём таблицы
    # create_db()

    # # генерируем данные
    # generate_database(1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000)
    
    # показываем таблицы 
    # show_all_table(10)

    # замеряем время всех запросов
    repertoire("Видимо", sort=True)
    cinema_address("Видимо", sort=True)
    free_places("Видимо", 1, sort=False)
    ticket_prices("Видимо", 1, sort=True)
    film_info("Ярко", sort=True)
    films_with_prizes(sort=False)
    comedy_on_day("2025-11-21", [1, 2, 3, 4, 5, 6, 7], sort=False)
   
if __name__ == "__main__":
    main()
