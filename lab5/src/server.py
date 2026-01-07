from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from sqlalchemy import create_engine, text
from datetime import datetime
import json

class RussJSON(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, ensure_ascii=False, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
    

DATABASE_URL = "postgresql+psycopg2://postgres:000000@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
app = Flask(__name__)
app.json = RussJSON(app) 
        
# Стартовая страница
@app.route("/")
def index():
    return """
    <h1>API LAB5 — тестовая панель</h1>

    <h2>Эндпоинты напрямую (Запросы из ЛБ3)</h2>
    <ul>
        <li> Запрос с уязвимостью: <a href="/repertoire?cinema_name=Аврора'%20OR%20'1'='1">/repertoire?cinema_name=Аврора'%20OR%20'1'='1</a></li>

        <li><a href="/repertoire?cinema_name=Аврора">/repertoire?cinema_name=Аврора</a></li>

        <li><a href="/cinema_address?cinema_name=Аврора">/cinema_address?cinema_name=Аврора</a></li>
        <li><a href="/free_seats?session_id=1">/free_seats?session_id=1</a></li>
        <li><a href="/ticket_prices?cinema_name=Аврора&session_id=1">/ticket_prices?cinema_name=Аврора&session_id=1</a></li>
        
        <li> Запрос с уязвимостью: <a href="/film_info?film_title=Барби%20OR%20'1'='1">/film_info?film_title=Барби%20OR%20'1'='1</a></li>
        <li><a href="/film_info?film_title=Барби">/film_info?film_title=Барби</a></li>
        <li><a href="/films_with_prizes">/films_with_prizes</a></li>
        <li><a href="/comedy_on_day?date=2025-10-21&session_ids=1,2,3,6,7">/comedy_on_day?date=2025-10-21&session_ids=1,2,3,6,7</a></li>

    </ul>

    <h2>Уязвимые запросы</h2>

    <h3>1. репертуар кинотеатра</h3>
    <form action="/repertoire" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра">
        <button type="submit">Отправить</button>
    </form>

    <h3>2. адрес кинотеатра</h3>
    <form action="/cinema_address" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра">
        <button type="submit">Отправить</button>
    </form>

    <h3>3. свободные места на сеанс</h3>
    <form action="/free_seats" method="get">
        <input name="session_id" placeholder="ID сеанса" type="number">
        <button type="submit">Отправить</button>
    </form>
    
    <hr>

    <h2>Безопасные запросы</h2>

    <h3>4. цены билетов на сеанс</h3>
    <form action="/ticket_prices" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра">
        <input name="session_id" placeholder="ID сеанса" type="number">
        <button type="submit">Отправить</button>
    </form>

    <h3>5. информация о фильме</h3>
    <form action="/film_info" method="get">
        <input name="film_title" placeholder="Название фильма">
        <button type="submit">Отправить</button>
    </form>

    <h3>6. фильмы с наградами</h3>
    <form action="/films_with_prizes" method="get">
        <button type="submit">Показать</button>
    </form>

    <h3>7. комедии по дням и сеансам</h3>
    <form action="/comedy_on_day" method="get">
        <input name="date" placeholder="Дата (YYYY-MM-DD)">
        <input name="session_ids" placeholder="ID сеансов (через запятую)">
        <button type="submit">Отправить</button>
    </form>

    <hr>
    
    """

# 1. репертуар кинотеатра (SQL-инъекция)
@app.route("/repertoire")
def repertoire():
    cinema_name = request.args.get("cinema_name", "")
    query = f"""
        SELECT DISTINCT f.title AS "Название фильма",
                        f.genre AS "Жанр",
                        f.director AS "Режиссер",
                        f.session_duration AS "Продолжительность (мин)"
        FROM films f
        JOIN sessions s ON f.film_id = s.film_id
        JOIN cinema_halls ch ON s.hall_id = ch.hall_id
        JOIN cinema c ON ch.cinema_id = c.cinema_id
        WHERE c.title = '{cinema_name}'        -- SQL-инъекция
    """
    with engine.connect() as conn:
        rows = [dict(r._mapping) for r in conn.execute(text(query))]
    return jsonify(rows)

# 2. адрес кинотеатра (SQL-инъекция)
@app.route("/cinema_address")
def cinema_address():
    cinema_name = request.args.get("cinema_name", "")
    query = text(f"""
        SELECT title AS "Кинотеатр",
               city_region AS "Район",
               address_cinema AS "Адрес"
        FROM cinema
        WHERE title = '{cinema_name}'        
    """)
    with engine.connect() as conn:
        rows = [dict(r._mapping) for r in conn.execute(query)]
    return jsonify(rows)

# 3. свободные места на сеанс (SQL-инъекция)
@app.route("/free_seats")
def free_seats():
    session_id = request.args.get("session_id", type=int)

    query = text(f"""
        SELECT COUNT(*) AS "Свободные места"
        FROM tickets t
        JOIN sessions s USING(session_id)
        WHERE s.session_id = {session_id} AND t.sold_out = '0';
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"sid": session_id})
        row = result.fetchone()

    return jsonify(row._asdict())


# 4. цены билетов на сеанс (безопасный запрос)
@app.route("/ticket_prices")
def get_ticket_prices():
    cinema_name = request.args.get("cinema_name", "")
    session_id = request.args.get("session_id", type=int)
    query = """
        SELECT DISTINCT 
            t.cost AS "Цена билета", 
            c.title AS "Кинотеатр", 
            TO_CHAR(s.start_time, 'HH24:MI:SS') AS "Время начала"  
        FROM tickets t
        JOIN sessions s ON t.session_id = s.session_id
        JOIN cinema_halls ch ON s.hall_id = ch.hall_id
        JOIN cinema c ON ch.cinema_id = c.cinema_id
        WHERE c.title = :cinema_name AND s.session_id = :session_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {"cinema_name": cinema_name, "session_id": session_id})
        rows = [dict(r._mapping) for r in result]
    return jsonify(rows)

# 5. информация о фильме (безопасный запрос)
@app.route("/film_info")
def film_info():
    film_title = request.args.get("film_title", "")
    query = text("""
        SELECT title AS "Фильм",
               genre AS "Жанр",
               production AS "Производство",
               director AS "Режиссер"
        FROM films
        WHERE title = :film_title
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {"film_title": film_title}).fetchone()

    return jsonify(dict(row._mapping) if row else {})

# 6. фильмы с наградами (безопасный запрос)
@app.route("/films_with_prizes")
def get_films_with_prizes():
    query = """
        SELECT 
            f.title AS "Фильм", 
            p.title AS "Награда", 
            fest.title AS "Фестиваль",
            TO_CHAR(s.date_session, 'YYYY-MM-DD') AS "Дата сеанса",  
            TO_CHAR(s.start_time, 'HH24:MI:SS') AS "Время начала",   
            c.title AS "Кинотеатр", 
            ch.title AS "Зал", 
            c.address_cinema AS "Адрес"
        FROM films f
        JOIN prizes p ON f.film_id = p.film_id
        JOIN festival fest ON p.festival_id = fest.festival_id
        JOIN sessions s ON f.film_id = s.film_id
        JOIN cinema_halls ch ON s.hall_id = ch.hall_id
        JOIN cinema c ON ch.cinema_id = c.cinema_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = [dict(r._mapping) for r in result]
    return jsonify(rows)

# 7. комедии по дням и сеансам (безопасный запрос)
@app.route("/comedy_on_day")
def comedy_on_day():
    date_str = request.args.get("date", "")
    session_ids_str = request.args.get("session_ids", "")
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    
    session_ids = []
    if session_ids_str:
        session_ids = [int(sid.strip()) for sid in session_ids_str.split(",") if sid.strip().isdigit()]
    
    if not date_obj or not session_ids:
        return jsonify({"error": "Необходимо указать дату и ID сеансов"}), 400
    
    query = text("""
        SELECT c.title "Кинотеатр", 
                f.title "Фильм", 
                f.genre "Жанр", 
                s.session_id "Сеанс", 
                ch.title "Название зала", 
                TO_CHAR(s.date_session, 'YYYY-MM-DD') AS "Дата сеанса",  
                TO_CHAR(s.start_time, 'HH24:MI:SS') AS "Время начала", 
                TO_CHAR(s.end_time, 'HH24:MI:SS') AS "Окончание сеанса"
        FROM sessions s
        JOIN films f USING(film_id)
        JOIN cinema_halls ch USING(hall_id)
        JOIN cinema c USING(cinema_id)
        WHERE f.genre = 'Комедия' 
            AND s.date_session = :date 
            AND s.session_id = ANY(:session_ids);
    """)
    
    with engine.connect() as conn:
        result = conn.execute(
            query, 
            {"date": date_obj, "session_ids": session_ids}
        )
        rows = [dict(row._mapping) for row in result]
    return jsonify(rows)
        
if __name__ == "__main__":
    app.run(debug=True, port=3000)
