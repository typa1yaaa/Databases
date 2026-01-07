-- -- -- Создание таблиц
-- -- CREATE TABLE Cinema (
-- --     cinema_id SERIAL PRIMARY KEY,
-- --     title VARCHAR(100) NOT NULL, 
-- --     city_region VARCHAR(100) NOT NULL,
-- --     address_cinema VARCHAR(100) NOT NULL,
-- --     category VARCHAR(30),
-- --     total_capacity INT NOT NULL CHECK (total_capacity > 0)
-- -- );

-- -- CREATE TABLE Films (
-- --     film_id SERIAL PRIMARY KEY,
-- --     title VARCHAR(100) NOT NULL, 
-- --     director VARCHAR(100) NOT NULL,
-- --     operator VARCHAR(100),
-- --     main_actors TEXT,
-- --     genre VARCHAR(30),
-- --     production VARCHAR(100),
-- --     session_duration INT NOT NULL CHECK (session_duration > 0),
-- --     shot_advertising VARCHAR(255)
-- -- );

-- -- CREATE TABLE Festival (
-- --     festival_id SERIAL PRIMARY KEY,
-- --     title VARCHAR(100) NOT NULL
-- -- );

-- -- CREATE TABLE Cinema_halls (
-- --     hall_id SERIAL PRIMARY KEY,
-- --     cinema_id INT NOT NULL,
-- --     title VARCHAR(100) NOT NULL, 
-- --     capacity INT NOT NULL CHECK (capacity > 0),
-- --     FOREIGN KEY (cinema_id) REFERENCES Cinema(cinema_id) ON DELETE CASCADE
-- -- );

-- -- CREATE TABLE Sessions(
-- --     session_id SERIAL PRIMARY KEY,
-- --     hall_id INT NOT NULL,
-- --     film_id INT NOT NULL,
-- --     date_session DATE NOT NULL,
-- --     start_time TIME NOT NULL,
-- --     end_time TIME NOT NULL,
-- --     FOREIGN KEY (hall_id) REFERENCES Cinema_halls(hall_id) ON DELETE CASCADE,
-- --     FOREIGN KEY (film_id) REFERENCES Films(film_id) ON DELETE CASCADE
-- -- );

-- -- CREATE TABLE Tickets (
-- --     ticket_id SERIAL PRIMARY KEY,
-- --     session_id INT NOT NULL,
-- --     row_number INT NOT NULL CHECK (row_number > 0),
-- --     place_number INT NOT NULL CHECK (place_number > 0),
-- --     sold_out BIT DEFAULT '0',
-- --     cost INT NOT NULL CHECK (cost >= 0),
-- --     FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE
-- -- );

-- -- CREATE TABLE Prizes (
-- --     prizes_id SERIAL PRIMARY KEY,
-- --     festival_id INT NOT NULL,
-- --     film_id INT NOT NULL,
-- --     title VARCHAR(100) NOT NULL, 
-- --     FOREIGN KEY (festival_id) REFERENCES Festival(festival_id) ON DELETE CASCADE,
-- --     FOREIGN KEY (film_id) REFERENCES Films(film_id) ON DELETE CASCADE
-- -- );

-- -- -- Заполнение таблиц
-- -- INSERT INTO Cinema (title, city_region, address_cinema, category, total_capacity) VALUES
-- -- ('Аврора', 'Центральный', 'Невский проспект, 60', 'Премиум', 600),
-- -- ('Формула Кино Галерея', 'Центральный', 'Лиговский проспект, 30', 'Мультиплекс', 800),
-- -- ('Каро 11 Охта Молл', 'Красногвардейский', 'Брантовская дорога, 3', 'Мультиплекс', 1200),
-- -- ('7D', 'Адмиралтейский', 'ул. Марата, 86', 'Классический', 280),
-- -- ('Ленфильм', 'Петроградский', 'Каменноостровский проспект, 10', 'Премиум', 450),
-- -- ('Дом кино', 'Центральный', 'ул. Караванная, 12', 'Исторический', 200),
-- -- ('Синема парк Питер Радуга', 'Московский', 'проспект Космонавтов, 14', 'Стандарт', 550),
-- -- ('Формула Кино Сити Молл', 'Приморский', 'Коломяжский проспект, 17', 'Стандарт', 320);

-- -- INSERT INTO Films (title, director, operator, main_actors, genre, production, session_duration, shot_advertising) VALUES
-- -- ('Аватар: Путь воды', 'Джеймс Кэмерон', 'Расселл Карпентер', 'Сэм Уортингтон, Зои Салдана, Стивен Лэнг, Кейт Уинслет', 'Фантастика', 'США', 192, 'avatar_water_poster.jpg'),
-- -- ('Оппенгеймер', 'Кристофер Нолан', 'Хойте ван Хойтема', 'Киллиан Мерфи, Эмили Блант, Мэтт Дэймон, Роберт Дауни-мл.', 'Исторический', 'США', 180, 'oppenheimer_poster.jpg'),
-- -- ('Дюна: Часть вторая', 'Дени Вильнёв', 'Грег Фрейзер', 'Тимоти Шаламе, Зендея, Ребекка Фергюсон, Остин Батлер', 'Фантастика', 'США', 166, 'dune2_poster.jpg'),
-- -- ('Барби', 'Грета Гервиг', 'Родриго Прието', 'Марго Робби, Райан Гослинг, Америка Феррера, Кейт МакКиннон', 'Комедия', 'США', 114, 'barbie_poster.jpg'),
-- -- ('Вызов', 'Клим Шипенко', 'Клим Шипенко', 'Юлия Пересильд, Владимир Машков, Михаил Трофимов', 'Драма', 'Россия', 165, 'challenge_poster.jpg'),
-- -- ('Человек-паук: Паутина вселенных', 'Жуакин Душ Сантуш', 'Джастин К. Томпсон', 'Шамеик Мур, Хейли Стайнфелд, Оскар Айзек', 'Мультфильм', 'США', 140, 'spiderverse_poster.jpg'),
-- -- ('Сергий против нечисти', 'Святослав Подгаевский', 'Святослав Подгаевский', 'Тихон Жизневский, Алексей Розин, Софья Райзман', 'Ужасы', 'Россия', 112, 'sergiy_poster.jpg'),
-- -- ('Гарри Поттер и Дары Смерти: Часть 2', 'Дэвид Йейтс', 'Эдуарду Серра', 'Дэниел Рэдклифф, Эмма Уотсон, Руперт Гринт, Рэйф Файнс', 'Фэнтези', 'Великобритания', 130, 'hp_deathly_hallows.jpg');

-- -- INSERT INTO Festival (title) VALUES
-- -- ('Каннский кинофестиваль'),
-- -- ('Оскар'),
-- -- ('Венецианский кинофестиваль'),
-- -- ('Берлинале'),
-- -- ('Кинотавр'),
-- -- ('Московский международный кинофестиваль'),
-- -- ('Сандэнс'),
-- -- ('Золотой орёл');

-- -- INSERT INTO Cinema_halls (cinema_id, title, capacity) VALUES
-- -- (1, 'Зал 1', 125),
-- -- (1, 'Зал 2', 75),
-- -- (2, 'Красный зал', 200),
-- -- (2, 'Синий зал', 100),
-- -- (2, 'Зеленый зал', 35),
-- -- (3, 'Основной зал', 150),
-- -- (4, 'Зал VIP', 15),
-- -- (4, 'Зал MEDIUM', 75);

-- -- INSERT INTO Sessions (hall_id, film_id, date_session, start_time, end_time) VALUES 
-- -- (1, 1, '2025-10-20', '10:00', '13:15'),
-- -- (1, 2, '2025-10-22', '14:00', '16:28'),
-- -- (1, 7, '2025-10-22', '17:00', '19:15'),
-- -- (3, 3, '2025-10-20', '11:30', '14:00'),
-- -- (4, 6, '2025-10-27', '11:30', '14:45'),
-- -- (5, 4, '2025-10-21', '15:00', '17:35'),
-- -- (5, 4, '2025-10-21', '18:15', '20:50'),
-- -- (6, 5, '2025-10-25', '12:00', '13:40');

-- -- INSERT INTO Tickets (session_id, row_number, place_number, sold_out, cost) VALUES
-- -- (1, 1, 5, '0', 350),
-- -- (1, 1, 6, '1', 270),
-- -- (2, 2, 3, '0', 400),
-- -- (3, 3, 15, '1', 250),
-- -- (4, 3, 9, '0', 370),
-- -- (5, 2, 13, '0', 250),
-- -- (6, 1, 12, '0', 500),
-- -- (7, 1, 7, '0', 1000);

-- -- INSERT INTO Prizes (festival_id, film_id, title) VALUES 
-- -- (2, 1, 'Лучшие визуальные эффекты'),
-- -- (1, 4, 'Золотая пальмовая ветвь'),
-- -- (3, 3, 'Лучшая режиссура'),
-- -- (2, 2, 'Лучший актер'),
-- -- (4, 5, 'Приз зрительских симпатий'),
-- -- (5, 6, 'Главный приз'),
-- -- (6, 7, 'Лучший фильм'),
-- -- (2, 8, 'Лучшая операторская работа');

-- -- -- Запрос для показа всех таблиц
-- -- SELECT * FROM Cinema;
-- -- SELECT * FROM Films;
-- -- SELECT * FROM Cinema_halls;
-- -- SELECT * FROM Sessions;
-- -- SELECT * FROM Tickets;
-- -- SELECT * FROM Prizes;
-- -- SELECT * FROM Festival;

-- Запросы из 1 лб
-- Репертуар кинотеатра? (кинотеатр Аврора)
SELECT DISTINCT f.title "Название фильма", f.genre "Жанр", f.director "Режиссер", f.session_duration "Продолжительность (мин)"
FROM Films f
JOIN Sessions s USING(film_id)
JOIN Cinema_halls ch USING(hall_id)
JOIN Cinema c USING(cinema_id)
WHERE c.title = 'Аврора'
ORDER BY f.title;

-- Адрес и район кинотеатра? (кинотеатр Аврора)
SELECT title "Кинотеатр", city_region "Район", address_cinema "Адрес"
FROM Cinema
WHERE title = 'Аврора';

-- Число свободных мест на данный сеанс в указанном кинотеатре? (кинотеатр Аврора, сеанс 1)
SELECT COUNT(*) "Свободные места на сеанс"
FROM Tickets t
JOIN Sessions s USING(session_id)
JOIN Cinema_halls ch USING(hall_id)
JOIN Cinema c USING(cinema_id)
WHERE c.title = 'Аврора' AND s.session_id = 1 AND t.sold_out = '0';

-- Цена билетов на данный сеанс в указанном кинотеатре? (кинотеатр Аврора, сеанс 1)
SELECT DISTINCT cost "Цена билета", c.title "Название кинотеатра", s.start_time "Время начала"
FROM Tickets t
JOIN Sessions s USING(session_id)
JOIN Cinema_halls ch USING(hall_id)
JOIN Cinema c USING(cinema_id)
WHERE c.title = 'Аврора' AND s.session_id = 1
ORDER BY cost;

-- Жанр, производство и режиссер данного фильма?
SELECT title "Фильм", genre "Жанр", production "Производство", director "Режиссер"
FROM Films
WHERE title = 'Барби';

-- Какие фильмы имеют награды, когда и в каких кинотеатрах они демонстрируются?
SELECT f.title "Фильм", p.title "Награда", fest.title "Фестиваль", s.date_session "Дата сеанса", s.start_time "Время начала", c.title "Кинотеатр", ch.title "Зал", c.address_cinema "Адрес кинотеатра"
FROM Prizes p
JOIN Films f USING(film_id)
JOIN Festival fest USING(festival_id)
JOIN Sessions s USING(film_id)
JOIN Cinema_halls ch USING(hall_id)
JOIN Cinema c USING(cinema_id) 
ORDER BY f.title, s.date_session, s.start_time;

-- В каких кинотеатрах в указанный день на указанных сеансах демонстрируется комедия? (день 2025-10-21, сеансы 1, 2, 3, 6 и 7)
SELECT c.title "Кинотеатр", f.title "Фильм", f.genre "Жанр", s.session_id "Сеанс", ch.title "Название зала", s.date_session "Дата", s.start_time "Начало сеанса", s.end_time "Окончание сеанса"
FROM Sessions s
JOIN Films f USING(film_id)
JOIN Cinema_halls ch USING(hall_id)
JOIN Cinema c USING(cinema_id)
WHERE f.genre = 'Комедия' AND s.date_session = '2025-10-21' AND s.session_id IN (1, 2, 3, 6, 7);