from create_table import *
from insert_data import *
from questions import *
from show_table import *
from delete_table import *

def main():
    # # удаляем таблицы 
    # delete_all_tables()

    # # cоздаём таблицы
    # create_db()
    # print("все таблицы созданы")

    # # # # показываем таблицы 
    # # show_all_table()

    # # вставляем данные
    # insert_cinemas()
    # insert_films()
    # insert_festivals()
    # insert_сinema_halls()
    # insert_sessions()
    # insert_tickets()
    # insert_prizes()
    # print("все данные успешно вставлены в базу")

    # показываем таблицы 
    show_all_table()

    # примеры запросов
    print("\n1. Репертуар кинотеатра? (кинотеатр Аврора)")
    print(repertoire("Аврора"))

    print("\n2. Адрес и район кинотеатра? (кинотеатр Аврора)")
    print(cinema_address("Аврора"))

    print("\n3. Число свободных мест на данный сеанс в указанном кинотеатре? (кинотеатр Аврора, сеанс 1)")
    print(free_places("Аврора", 1))

    print("\n4. Цена билетов на данный сеанс в указанном кинотеатре? (кинотеатр Аврора, сеанс 1)")
    print(ticket_prices("Аврора", 1))

    print("\n5. Жанр, производство и режиссер данного фильма? (Барби)")
    print(film_info("Барби"))

    print("\n6. Какие фильмы имеют награды, когда и в каких кинотеатрах они демонстрируются?")
    print(films_with_prizes())

    print("\n7.  В каких кинотеатрах в указанный день на указанных сеансах демонстрируется комедия? (день 2025-10-21, сеансы 1, 2, 3, 6 и 7)")
    print(comedy_on_day("2025-10-21", [1,2,3,6,7]))

if __name__ == "__main__":
    main()
