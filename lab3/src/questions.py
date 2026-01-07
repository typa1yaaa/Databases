from sqlalchemy import func, distinct
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
from models import *
from db_config import *

def repertoire(cinema_name):
    result = (session.query(distinct(Films.title), Films.genre, Films.director, Films.session_duration)
              .join(Sessions, Films.film_id == Sessions.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Cinema.title == cinema_name)
              .order_by(Films.title)
              .all())
    
    headers = ["Название фильма", "Жанр", "Режиссер", "Продолжительность (мин)"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")

def cinema_address(cinema_name):
    result = session.query(Cinema.title, Cinema.city_region, Cinema.address_cinema)\
        .filter(Cinema.title == cinema_name).first()
    
    headers = ["Кинотеатр", "Район", "Адрес"]
    return tabulate([result], headers=headers, tablefmt="fancy_grid")

def free_places(cinema_name, session_id):
    count = (session.query(func.count(Tickets.ticket_id))
             .join(Sessions)
             .join(CinemaHalls)
             .join(Cinema)
             .filter(Cinema.title == cinema_name, Sessions.session_id == session_id, Tickets.sold_out == '0')
             .scalar())
    headers = ["Свободные места"]
    return tabulate([[count]], headers=headers, tablefmt="fancy_grid")

def ticket_prices(cinema_name, session_id):
    result = (session.query(distinct(Tickets.cost), Cinema.title, Sessions.start_time)
              .join(Sessions, Tickets.session_id == Sessions.session_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Cinema.title == cinema_name, Sessions.session_id == session_id)
              .order_by(Tickets.cost)
              .all())
    
    headers = ["Цена билета", "Название кинотеатра", "Время начала"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")

def film_info(film_title):
    result = session.query(Films.title, Films.genre, Films.production, Films.director)\
        .filter(Films.title == film_title).first()

    headers = ["Фильм", "Жанр", "Производство", "Режиссер"]
    return tabulate([result], headers=headers, tablefmt="fancy_grid")

def films_with_prizes():
    result = (session.query(Films.title, Prizes.title.label("Награда"), Festival.title.label("Фестиваль"),
                            Sessions.date_session, Sessions.start_time,
                            Cinema.title.label("Кинотеатр"), CinemaHalls.title.label("Зал"),
                            Cinema.address_cinema)
              .join(Prizes, Films.film_id == Prizes.film_id)
              .join(Festival, Prizes.festival_id == Festival.festival_id)
              .join(Sessions, Films.film_id == Sessions.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .order_by(Films.title, Sessions.date_session, Sessions.start_time)
              .all())
    
    headers = ["Фильм", "Награда", "Фестиваль", "Дата сеанса", "Время начала", "Кинотеатр", "Зал", "Адрес"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")

def comedy_on_day(date, session_ids):
    result = (session.query(Cinema.title.label("Кинотеатр"), Films.title.label("Фильм"), Films.genre,
                            Sessions.session_id, CinemaHalls.title.label("Зал"),
                            Sessions.date_session, Sessions.start_time, Sessions.end_time)
              .join(Films, Sessions.film_id == Films.film_id)
              .join(CinemaHalls, Sessions.hall_id == CinemaHalls.hall_id)
              .join(Cinema, CinemaHalls.cinema_id == Cinema.cinema_id)
              .filter(Films.genre == 'Комедия', Sessions.date_session == date,
                      Sessions.session_id.in_(session_ids))
              .all())
    
    headers = ["Кинотеатр", "Фильм", "Жанр", "Сеанс", "Зал", "Дата", "Начало", "Окончание"]
    return tabulate(result, headers=headers, tablefmt="fancy_grid")