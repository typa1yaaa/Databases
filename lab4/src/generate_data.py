from faker import Faker
from random import randint, choice
from datetime import timedelta
import math
from db_config import Session
from models import Cinema, Films, Festival, CinemaHalls, Sessions, Tickets, Prizes

fake = Faker("ru_RU")

def generate_cinemas(n):
    data = []
    for _ in range(n):
        data.append(Cinema(
            title=fake.word().capitalize(),
            city_region=f"{fake.word().capitalize()} район",
            address_cinema=fake.address().replace("\n", ", "),
            category=choice(["премиум", "обычный", "семейный", "IMAX"]),
            total_capacity=randint(150, 900)
        ))
   
    return data

def generate_halls(cinemas, max_halls_total):
    halls = []
    total_halls_created = 0
     
    # каждому кинотеатру даем хотя бы по 1 залу
    for cinema in cinemas:
        if total_halls_created >= max_halls_total:
            break
        hall_capacity = randint(50, 200)
        hall_number = randint(1, 30)
        halls.append(CinemaHalls(
            cinema=cinema,
            title=f"Зал {hall_number}",
            capacity=hall_capacity
        ))
        total_halls_created += 1

    # распределяем оставшиеся залы случайно
    remaining_halls = max_halls_total - total_halls_created
    
    while remaining_halls > 0:
        cinema = choice(cinemas)
        hall_capacity = randint(50, 200)
        hall_number = randint(1, 30)
        halls.append(CinemaHalls(
            cinema=cinema,
            title=f"Зал {hall_number}",
            capacity=hall_capacity
        ))
        total_halls_created += 1
        remaining_halls -= 1

    return halls

def generate_films(n):
    films = []
    for _ in range(n):
        films.append(Films(
            title=" ".join(fake.words(nb=randint(1, 3))).title(),
            director=fake.name(),
            operator=fake.name(),
            main_actors=", ".join(fake.name() for _ in range(3)),
            genre=choice(["Комедия", "Драма", "Боевик", "Фантастика", "Ужасы", "Триллер", "Мелодрама", "Биография"]),
            production=fake.country(),
            session_duration=randint(60, 200),
            shot_advertising=fake.file_name(extension="jpg")
        ))

    return films

def generate_festivals(n):
    festivals = []
    for _ in range(n):
        festivals.append(Festival(
            title=f"{fake.word().capitalize()} фестиваль"
        ))

    return festivals

def generate_sessions(films, halls, n, session_obj):
    sessions = []
    for _ in range(n):
        film = choice(films)
        hall = choice(halls)

        start = fake.date_time_between(start_date="-30d", end_date="+30d")
        end = start + timedelta(minutes=film.session_duration)

        sess = Sessions(
            hall=hall, 
            film=film,
            date_session=start.date(),
            start_time=start.time(),
            end_time=end.time()
        )
        sessions.append(sess)
        session_obj.add(sess)

    session_obj.commit()
    return sessions

def generate_tickets(sessions, session_obj, max_tickets=None, max_rows=15):
    tickets = []
    total_generated = 0

    for sess in sessions:
        hall_capacity = sess.hall.capacity
        
        rows = randint(1, max_rows)
        places_per_row = math.ceil(hall_capacity / rows)

        tickets_for_session = min(hall_capacity, max_tickets - total_generated) if max_tickets else hall_capacity
        
        for _ in range(tickets_for_session):
            row = randint(1, rows)
            place = randint(1, places_per_row)

            ticket = Tickets(
                session=sess,
                row_number=row,
                place_number=place,
                sold_out=choice(["0", "1"]),
                cost=choice([300, 400, 500, 600])
            )
            tickets.append(ticket)
            session_obj.add(ticket)
            total_generated += 1

        if max_tickets and total_generated >= max_tickets:
            break

    session_obj.commit()
    return tickets

def generate_prizes(films, festivals, prizes_n):
    prizes = []
    for _ in range(prizes_n):
        prizes.append(Prizes(
            film=choice(films),
            festival=choice(festivals),
            title=fake.word().capitalize() + " приз"
        ))
    return prizes

def generate_database(cinemas_n=100, max_halls_total = 100, max_tickets=100, films_n=100, prizes_n=100,festivals_n=100, sessions_n=100):
    session = Session()
    print("генерация кинотеатров...")
    cinemas = generate_cinemas(cinemas_n)
    session.add_all(cinemas)
    session.commit()

    print("генерация фильмов...")
    films = generate_films(films_n)
    session.add_all(films)
    session.commit()
    
    print("генерация залов...")
    halls = generate_halls(cinemas, max_halls_total)
    session.add_all(halls)
    session.commit()

    print("генерация фестивалей...")
    festivals = generate_festivals(festivals_n)
    session.add_all(festivals)
    session.commit()

    print("генерация сеансов...")
    sessions = generate_sessions(films, halls, sessions_n, session)
    
    print("генерация билетов...")
    tickets = generate_tickets(sessions, session, max_tickets)

    print("генерация наград...")
    prizes = generate_prizes(films, festivals,prizes_n)
    session.add_all(prizes)
    session.commit()