from models import *
from db_config import *

def insert_cinemas():
    cinemas = [
        Cinema(title='Аврора', city_region='Центральный', address_cinema='Невский проспект, 60', category='Премиум', total_capacity=600),
        Cinema(title='Формула Кино Галерея', city_region='Центральный', address_cinema='Лиговский проспект, 30', category='Мультиплекс', total_capacity=800),
        Cinema(title='Каро 11 Охта Молл', city_region='Красногвардейский', address_cinema='Брантовская дорога, 3', category='Мультиплекс', total_capacity=1200),
        Cinema(title='7D', city_region='Адмиралтейский', address_cinema='ул. Марата, 86', category='Классический', total_capacity=280),
        Cinema(title='Ленфильм', city_region='Петроградский', address_cinema='Каменноостровский проспект, 10', category='Премиум', total_capacity=450),
        Cinema(title='Дом кино', city_region='Центральный', address_cinema='ул. Караванная, 12', category='Исторический', total_capacity=200),
        Cinema(title='Синема парк Питер Радуга', city_region='Московский', address_cinema='проспект Космонавтов, 14', category='Стандарт', total_capacity=550),
        Cinema(title='Формула Кино Сити Молл', city_region='Приморский', address_cinema='Коломяжский проспект, 17', category='Стандарт', total_capacity=320),
    ]
    session.add_all(cinemas)
    session.commit()
    print("таблица Cinema заполнена")

def insert_films():
    films = [
        Films(title='Аватар: Путь воды', director='Джеймс Кэмерон', operator='Расселл Карпентер', main_actors='Сэм Уортингтон, Зои Салдана, Стивен Лэнг, Кейт Уинслет', genre='Фантастика', production='США', session_duration=192, shot_advertising='avatar_water_poster.jpg'),
        Films(title='Оппенгеймер', director='Кристофер Нолан', operator='Хойте ван Хойтема', main_actors='Киллиан Мерфи, Эмили Блант, Мэтт Дэймон, Роберт Дауни-мл.', genre='Исторический', production='США', session_duration=180, shot_advertising='oppenheimer_poster.jpg'),
        Films(title='Дюна: Часть вторая', director='Дени Вильнёв', operator='Грег Фрейзер', main_actors='Тимоти Шаламе, Зендея, Ребекка Фергюсон, Остин Батлер', genre='Фантастика', production='США', session_duration=166, shot_advertising='dune2_poster.jpg'),
        Films(title='Барби', director='Грета Гервиг', operator='Родриго Прието', main_actors='Марго Робби, Райан Гослинг, Америка Феррера, Кейт МакКиннон', genre='Комедия', production='США', session_duration=114, shot_advertising='barbie_poster.jpg'),
        Films(title='Вызов', director='Клим Шипенко', operator='Клим Шипенко', main_actors='Юлия Пересильд, Владимир Машков, Михаил Трофимов', genre='Драма', production='Россия', session_duration=165, shot_advertising='challenge_poster.jpg'),
        Films(title='Человек-паук: Паутина вселенных', director='Жуакин Душ Сантуш', operator='Джастин К. Томпсон', main_actors='Шамеик Мур, Хейли Стайнфелд, Оскар Айзек', genre='Мультфильм', production='США', session_duration=140, shot_advertising='spiderverse_poster.jpg'),
        Films(title='Сергий против нечисти', director='Святослав Подгаевский', operator='Святослав Подгаевский', main_actors='Тихон Жизневский, Алексей Розин, Софья Райзман', genre='Ужасы', production='Россия', session_duration=112, shot_advertising='sergiy_poster.jpg'),
        Films(title='Гарри Поттер и Дары Смерти: Часть 2', director='Дэвид Йейтс', operator='Эдуарду Серра', main_actors='Дэниел Рэдклифф, Эмма Уотсон, Руперт Гринт, Рэйф Файнс', genre='Фэнтези', production='Великобритания', session_duration=130, shot_advertising='hp_deathly_hallows.jpg')
    ]
    session.add_all(films)
    session.commit()
    print("таблица Films заполнена")

def insert_festivals():
    festivals = [
        Festival(title='Каннский кинофестиваль'),
        Festival(title='Оскар'),
        Festival(title='Венецианский кинофестиваль'),
        Festival(title='Берлинале'),
        Festival(title='Кинотавр'),
        Festival(title='Московский международный кинофестиваль'),
        Festival(title='Сандэнс'),
        Festival(title='Золотой орёл')
    ]
    session.add_all(festivals)
    session.commit()
    print("таблица Festival заполнена")

def insert_сinema_halls():
    halls = [
        CinemaHalls(cinema_id=1, title='Зал 1', capacity=125),
        CinemaHalls(cinema_id=1, title='Зал 2', capacity=75),
        CinemaHalls(cinema_id=2, title='Красный зал', capacity=200),
        CinemaHalls(cinema_id=2, title='Синий зал', capacity=100),
        CinemaHalls(cinema_id=2, title='Зеленый зал', capacity=35),
        CinemaHalls(cinema_id=3, title='Основной зал', capacity=150),
        CinemaHalls(cinema_id=4, title='Зал VIP', capacity=15),
        CinemaHalls(cinema_id=4, title='Зал MEDIUM', capacity=75)
    ]
    session.add_all(halls)
    session.commit()
    print("таблица CinemaHalls заполнена")

def insert_sessions():
    sessions_list = [
        Sessions(hall_id=1, film_id=1, date_session='2025-10-20', start_time='10:00', end_time='13:15'),
        Sessions(hall_id=1, film_id=2, date_session='2025-10-22', start_time='14:00', end_time='16:28'),
        Sessions(hall_id=1, film_id=7, date_session='2025-10-22', start_time='17:00', end_time='19:15'),
        Sessions(hall_id=3, film_id=3, date_session='2025-10-20', start_time='11:30', end_time='14:00'),
        Sessions(hall_id=4, film_id=6, date_session='2025-10-27', start_time='11:30', end_time='14:45'),
        Sessions(hall_id=5, film_id=4, date_session='2025-10-21', start_time='15:00', end_time='17:35'),
        Sessions(hall_id=5, film_id=4, date_session='2025-10-21', start_time='18:15', end_time='20:50'),
        Sessions(hall_id=6, film_id=5, date_session='2025-10-25', start_time='12:00', end_time='13:40')
    ]
    session.add_all(sessions_list)
    session.commit()
    print("таблица Sessions заполнена")

def insert_tickets():
    tickets_list = [
        Tickets(session_id=1, row_number=1, place_number=5, sold_out='0', cost=350),
        Tickets(session_id=1, row_number=1, place_number=6, sold_out='1', cost=270),
        Tickets(session_id=2, row_number=2, place_number=3, sold_out='0', cost=400),
        Tickets(session_id=3, row_number=3, place_number=15, sold_out='1', cost=250),
        Tickets(session_id=4, row_number=3, place_number=9, sold_out='0', cost=370),
        Tickets(session_id=5, row_number=2, place_number=13, sold_out='0', cost=250),
        Tickets(session_id=6, row_number=1, place_number=12, sold_out='0', cost=500),
        Tickets(session_id=7, row_number=1, place_number=7, sold_out='0', cost=1000)
    ]
    session.add_all(tickets_list)
    session.commit()
    print("таблица Tickets заполнена")

def insert_prizes():
    prizes_list = [
        Prizes(festival_id=2, film_id=1, title='Лучшие визуальные эффекты'),
        Prizes(festival_id=1, film_id=4, title='Золотая пальмовая ветвь'),
        Prizes(festival_id=3, film_id=3, title='Лучшая режиссура'),
        Prizes(festival_id=2, film_id=2, title='Лучший актер'),
        Prizes(festival_id=4, film_id=5, title='Приз зрительских симпатий'),
        Prizes(festival_id=5, film_id=6, title='Главный приз'),
        Prizes(festival_id=6, film_id=7, title='Лучший фильм'),
        Prizes(festival_id=2, film_id=8, title='Лучшая операторская работа')
    ]
    session.add_all(prizes_list)
    session.commit()
    print("таблица Prizes заполнена")

def insert_all_data():
    insert_cinemas()
    insert_films()
    insert_festivals()
    insert_сinema_halls()
    insert_sessions()
    insert_tickets()
    insert_prizes()
    print("все данные успешно вставлены в базу")
