import time
from questions import *
from db_config import session
from models import *

def measure_time(func, *args, repeats=25, **kwargs):
    total = 0
    result_preview = None

    for _ in range(repeats):
        start = time.perf_counter()
        result_preview = func(*args, **kwargs)
        session.expire_all()
        end = time.perf_counter()
        total += (end - start)

    avg_time = total / repeats
    return avg_time, result_preview

def pick_any(query):
    obj = query.first()
    if obj is None:
        raise ValueError("таблица пуста")
    return obj


def measure_all():
    any_cinema = pick_any(session.query(Cinema)).title
    any_film = pick_any(session.query(Films)).title
    any_session = pick_any(session.query(Sessions)).session_id

    session_ids = [s.session_id for s in session.query(Sessions).limit(5)]
    date_any = pick_any(session.query(Sessions)).date_session

    tests = [
        ("Запрос 1", repertoire, (any_cinema,)),
        ("Запрос 2", cinema_address, (any_cinema,)),
        ("Запрос 3", free_places, (any_cinema, any_session)),
        ("Запрос 4", ticket_prices, (any_cinema, any_session)),
        ("Запрос 5", film_info, (any_film,)),
        ("Запрос 6", films_with_prizes, ()),
        ("Запрос 7", comedy_on_day, (date_any, session_ids)),
    ]

    for title, func, args in tests:
        exec_time, _ = measure_time(func, *args,  sort=False)
        print(f"{title:35} — без сортировки: {exec_time:.6f} сек")

        exec_time, _ = measure_time(func, *args,  sort=True)
        print(f"{title:35} — с сортировкой: {exec_time:.6f} сек")
        print("-" * 60)


if __name__ == "__main__":
    measure_all()