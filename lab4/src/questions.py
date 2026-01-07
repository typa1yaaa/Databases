from sqlalchemy import func, distinct
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from models import *
from db_config import *
import time

def repertoire(cinema_name, sort=False, limit=None):
    start = time.perf_counter()
    query = (session.query(distinct(Films.title), Films.genre, Films.director, Films.session_duration)
              .join(Sessions, Films.film_id == Sessions.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Cinema.title == cinema_name))

    end = time.perf_counter()
    print("Время выполения запроса 1 БЕЗ СОРТИРОВКИ: ", end - start)

    if sort:
        query = query.order_by(Films.title)

    end = time.perf_counter()
    print("Время выполения запроса 1 C СОРТИРОВКОЙ: ", end - start)

    if limit is not None:
        query = query.limit(limit)

    result = query.all()

    headers = ["Название фильма", "Жанр", "Режиссер", "Продолжительность (мин)"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")


def cinema_address(cinema_name, sort=False, limit=None):
    start = time.perf_counter()
    query = session.query(Cinema.title, Cinema.city_region, Cinema.address_cinema)\
        .filter(Cinema.title == cinema_name)
    
    end = time.perf_counter()
    print("Время выполения запроса 2 БЕЗ СОРТИРОВКИ: ", end - start)

    if sort:
        query = query.order_by(Cinema.title)

    end = time.perf_counter()
    print("Время выполения запроса 2 C СОРТИРОВКОЙ: ", end - start)

    if limit is not None:
        query = query.limit(limit)

    result = query.first()

    headers = ["Кинотеатр", "Район", "Адрес"]
    return tabulate([result], headers=headers, tablefmt="fancy_grid")


def free_places(cinema_name, session_id, sort=False, limit=None):
    start = time.perf_counter()
    query = (session.query(func.count(Tickets.ticket_id))
             .join(Sessions)
             .join(CinemaHalls)
             .join(Cinema)
             .filter(Cinema.title == cinema_name, Sessions.session_id == session_id, Tickets.sold_out == '0'))
    
    end = time.perf_counter()
    print("Время выполения запроса 3 БЕЗ СОРТИРОВКИ: ", end - start)

    if limit is not None:
        query = query.limit(limit)
        
    count = query.scalar()

    headers = ["Свободные места"]
    return tabulate([[count]], headers=headers, tablefmt="fancy_grid")


def ticket_prices(cinema_name, session_id, sort=False, limit=None):
    start = time.perf_counter()
    query = (session.query(distinct(Tickets.cost), Cinema.title, Sessions.start_time)
              .join(Sessions, Tickets.session_id == Sessions.session_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Cinema.title == cinema_name, Sessions.session_id == session_id))
    
    end = time.perf_counter()
    print("Время выполения запроса 4 БЕЗ СОРТИРОВКИ: ", end - start)
    
    if sort:
        query = query.order_by(Tickets.cost)

    end = time.perf_counter()
    print("Время выполения запроса 4 С СОРТИРОВКОЙ: ", end - start)
    
    if limit is not None:
        query = query.limit(limit)

    result = query.all()    

    headers = ["Цена билета", "Название кинотеатра", "Время начала"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")


def film_info(film_title, sort=False, limit=None):
    start = time.perf_counter()
    query = session.query(Films.title, Films.genre, Films.production, Films.director)\
        .filter(Films.title == film_title)

    end = time.perf_counter()
    print("Время выполения запроса 5 БЕЗ СОРТИРОВКИ: ", end - start)

    if limit is not None:
        query = query.limit(limit)

    result = query.first()

    headers = ["Фильм", "Жанр", "Производство", "Режиссер"]
    return tabulate([result], headers=headers, tablefmt="fancy_grid")


def films_with_prizes(sort=False, limit=None):
    start = time.perf_counter()
    query = (session.query(Films.title, Prizes.title.label("Награда"), Festival.title.label("Фестиваль"),
                            Sessions.date_session, Sessions.start_time,
                            Cinema.title.label("Кинотеатр"), CinemaHalls.title.label("Зал"),
                            Cinema.address_cinema)
              .join(Prizes, Films.film_id == Prizes.film_id)
              .join(Festival, Prizes.festival_id == Festival.festival_id)
              .join(Sessions, Films.film_id == Sessions.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id))
    
    end = time.perf_counter()
    print("Время выполения запроса 6 БЕЗ СОРТИРОВКИ: ", end - start)

    if sort:
        query = query.order_by(Films.title, Sessions.date_session, Sessions.start_time)

    end = time.perf_counter()
    print("Время выполения запроса 6 С СОРТИРОВКОЙ: ", end - start)

    if limit is not None:
        query = query.limit(limit)

    result = query.all()

    headers = ["Фильм", "Награда", "Фестиваль", "Дата сеанса", "Время начала", "Кинотеатр", "Зал", "Адрес"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")


def comedy_on_day(date, session_ids, sort=False, limit=None):
    start = time.perf_counter()
    query = (session.query(Cinema.title.label("Кинотеатр"), Films.title.label("Фильм"), Films.genre,
                            Sessions.session_id, CinemaHalls.title.label("Зал"),
                            Sessions.date_session, Sessions.start_time, Sessions.end_time)
              .join(Films, Sessions.film_id == Films.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Films.genre == 'Комедия', Sessions.date_session == date,
                      Sessions.session_id.in_(session_ids)))
    
    end = time.perf_counter()
    print("Время выполения запроса 7 БЕЗ СОРТИРОВКИ: ", end - start)

    if sort:
        query = query.order_by(Sessions.start_time)

    end = time.perf_counter()
    print("Время выполения запроса 7 С СОРТИРОВКОЙ: ", end - start)

    if limit is not None:
        query = query.limit(limit)

    result = query.all()

    headers = ["Кинотеатр", "Фильм", "Жанр", "Сеанс", "Зал", "Дата", "Начало", "Окончание"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")




def all_questions():
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