from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
import json
from datetime import datetime, date, time
from decimal import Decimal

# Кастомный JSON провайдер для обработки объектов date, time и Decimal
class PrettyJSON:
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
    
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=self.default, ensure_ascii=False, **kwargs)
    
    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

DATABASE_URL = "postgresql+psycopg2://postgres:000000@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
app = Flask(__name__)
app.json = PrettyJSON()

# Вспомогательная функция для преобразования результатов
def convert_row_to_dict(row):
    """Преобразует строку результата в словарь с сериализуемыми значениями"""
    result = {}
    for key, value in row._mapping.items():
        if isinstance(value, (date, datetime)):
            result[key] = value.isoformat()
        elif isinstance(value, time):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = float(value)
        else:
            result[key] = value
    return result

# ---------------------------
# Стартовая страница
# ---------------------------
@app.route("/")
def index():
    return """
    <h1>Lab5 API — тестовая панель (Flask + SQL-инъекции)</h1>

    <h2>Уязвимые запросы (с SQL-инъекциями)</h2>

    <h3>1. Репертуар кинотеатра (УЯЗВИМЫЙ)</h3>
    <form action="/repertoire" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра" value="Аврора">
        <button type="submit">Отправить</button>
    </form>

    <h3>2. Адрес кинотеатра (УЯЗВИМЫЙ)</h3>
    <form action="/cinema_address" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра" value="Аврора">
        <button type="submit">Отправить</button>
    </form>

    <h3>3. Свободные места на сеанс (УЯЗВИМЫЙ)</h3>
    <form action="/free_seats" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра" value="Аврора">
        <input name="session_id" placeholder="ID сеанса" value="1">
        <button type="submit">Отправить</button>
    </form>

    <hr>

    <h2>Безопасные запросы</h2>

    <h3>4. Цены билетов на сеанс</h3>
    <form action="/ticket_prices" method="get">
        <input name="cinema_name" placeholder="Название кинотеатра" value="Аврора">
        <input name="session_id" placeholder="ID сеанса" value="1" type="number">
        <button type="submit">Отправить</button>
    </form>

    <h3>5. Информация о фильме</h3>
    <form action="/film_info" method="get">
        <input name="film_title" placeholder="Название фильма" value="Барби">
        <button type="submit">Отправить</button>
    </form>

    <h3>6. Фильмы с наградами</h3>
    <form action="/films_with_prizes" method="get">
        <button type="submit">Показать все фильмы с наградами</button>
    </form>

    <h3>7. Комедии по дням и сеансам</h3>
    <form action="/comedy_on_day" method="get">
        <input name="date" placeholder="Дата (YYYY-MM-DD)" value="2025-10-21">
        <input name="session_ids" placeholder="ID сеансов через запятую" value="1,2,3,6,7">
        <button type="submit">Отправить</button>
    </form>

    <hr>
    <h2>Эндпоинты напрямую</h2>
    <ul>
        <li><a href="/repertoire?cinema_name=Аврора">/repertoire?cinema_name=Аврора</a></li>
        <li><a href="/cinema_address?cinema_name=Аврора">/cinema_address?cinema_name=Аврора</a></li>
        <li><a href="/free_seats?cinema_name=Аврора&session_id=1">/free_seats?cinema_name=Аврора&session_id=1</a></li>
        <li><a href="/ticket_prices?cinema_name=Аврора&session_id=1">/ticket_prices?cinema_name=Аврора&session_id=1</a></li>
        <li><a href="/film_info?film_title=Барби">/film_info?film_title=Барби</a></li>
        <li><a href="/films_with_prizes">/films_with_prizes</a></li>
        <li><a href="/comedy_on_day?date=2025-10-21&session_ids=1,2,3,6,7">/comedy_on_day?date=2025-10-21&session_ids=1,2,3,6,7</a></li>
    </ul>
    """

# 1. Репертуар кинотеатра (УЯЗВИМЫЙ запрос - SQL-инъекция)
@app.route("/repertoire")
def repertoire():
    cinema_name = request.args.get("cinema_name", "")
    
    # УЯЗВИМЫЙ ЗАПРОС - прямое внедрение параметра
    query = f"""
        SELECT DISTINCT f.title "Название фильма", 
                       f.genre "Жанр", 
                       f.director "Режиссер", 
                       f.session_duration "Продолжительность (мин)"
        FROM films f
        JOIN sessions s USING(film_id)
        JOIN cinema_halls ch USING(hall_id)
        JOIN cinema c USING(cinema_id)
        WHERE c.title = '{cinema_name}'
        ORDER BY f.title;
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [convert_row_to_dict(row) for row in result]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Адрес кинотеатра (УЯЗВИМЫЙ запрос - SQL-инъекция)
@app.route("/cinema_address")
def cinema_address():
    cinema_name = request.args.get("cinema_name", "")
    
    # УЯЗВИМЫЙ ЗАПРОС - прямое внедрение параметра
    query = f"""
        SELECT title "Кинотеатр", 
               city_region "Район", 
               address_cinema "Адрес"
        FROM cinema
        WHERE title = '{cinema_name}';
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [convert_row_to_dict(row) for row in result]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Свободные места на сеанс (УЯЗВИМЫЙ запрос - SQL-инъекция)
@app.route("/free_seats")
def free_seats():
    cinema_name = request.args.get("cinema_name", "Аврора")
    session_id = request.args.get("session_id", "")
    
    # УЯЗВИМЫЙ ЗАПРОС - прямое внедрение параметра session_id
    query = f"""
        SELECT COUNT(*) "Свободные места на сеанс"
        FROM tickets t
        JOIN sessions s USING(session_id)
        JOIN cinema_halls ch USING(hall_id)
        JOIN cinema c USING(cinema_id)
        WHERE c.title = '{cinema_name}' 
          AND s.session_id = {session_id if session_id else 'NULL'} 
          AND t.sold_out = '0';
    """
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            row = result.fetchone()
            if row:
                return jsonify(convert_row_to_dict(row))
            else:
                return jsonify({"Свободные места на сеанс": 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Цена билетов на данный сеанс (БЕЗОПАСНЫЙ запрос)
@app.route("/ticket_prices")
def ticket_prices():
    cinema_name = request.args.get("cinema_name", "")
    session_id = request.args.get("session_id", "")
    
    # БЕЗОПАСНЫЙ ЗАПРОС - параметризация
    query = text("""
        SELECT DISTINCT cost "Цена билета", 
               c.title "Название кинотеатра", 
               s.start_time "Время начала"
        FROM tickets t
        JOIN sessions s USING(session_id)
        JOIN cinema_halls ch USING(hall_id)
        JOIN cinema c USING(cinema_id)
        WHERE c.title = :cinema_name 
          AND s.session_id = :session_id
        ORDER BY cost;
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(
                query, 
                {"cinema_name": cinema_name, "session_id": session_id}
            )
            rows = [convert_row_to_dict(row) for row in result]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. Информация о фильме (БЕЗОПАСНЫЙ запрос)
@app.route("/film_info")
def film_info():
    film_title = request.args.get("film_title", "")
    
    # БЕЗОПАСНЫЙ ЗАПРОС - параметризация
    query = text("""
        SELECT title "Фильм", 
               genre "Жанр", 
               production "Производство", 
               director "Режиссер"
        FROM films
        WHERE title = :film_title;
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"film_title": film_title})
            row = result.fetchone()
            if row:
                return jsonify(convert_row_to_dict(row))
            else:
                return jsonify({})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6. Фильмы с наградами (БЕЗОПАСНЫЙ запрос)
@app.route("/films_with_prizes")
def get_films_with_prizes():
    # БЕЗОПАСНЫЙ ЗАПРОС - без параметров
    query = text("""
        SELECT f.title AS "Фильм", 
               p.title AS "Награда", 
               fest.title AS "Фестиваль",
               s.date_session AS "Дата сеанса", 
               s.start_time AS "Время начала",
               c.title AS "Кинотеатр", 
               ch.title AS "Зал", 
               c.address_cinema AS "Адрес"
        FROM films f
        JOIN prizes p ON f.film_id = p.film_id
        JOIN festival fest ON p.festival_id = fest.festival_id
        JOIN sessions s ON f.film_id = s.film_id
        JOIN cinema_halls ch ON s.hall_id = ch.hall_id
        JOIN cinema c ON ch.cinema_id = c.cinema_id
        ORDER BY f.title, s.date_session, s.start_time
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            rows = [convert_row_to_dict(row) for row in result]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 7. Комедии по дням и сеансам (БЕЗОПАСНЫЙ запрос)
@app.route("/comedy_on_day")
def comedy_on_day():
    date_str = request.args.get("date", "")
    session_ids_str = request.args.get("session_ids", "")
    
    try:
        # Парсим дату
        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            return jsonify({"error": "Необходимо указать дату"}), 400
        
        # Парсим список ID сеансов
        session_ids = []
        if session_ids_str:
            session_ids = [int(sid.strip()) for sid in session_ids_str.split(",") if sid.strip().isdigit()]
        
        if not session_ids:
            return jsonify({"error": "Необходимо указать ID сеансов"}), 400
        
        # БЕЗОПАСНЫЙ ЗАПРОС - параметризация
        query = text("""
            SELECT c.title "Кинотеатр", 
                   f.title "Фильм", 
                   f.genre "Жанр", 
                   s.session_id "Сеанс", 
                   ch.title "Название зала", 
                   s.date_session "Дата", 
                   s.start_time "Начало сеанса", 
                   s.end_time "Окончание сеанса"
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
            rows = [convert_row_to_dict(row) for row in result]
        return jsonify(rows)
        
    except ValueError as e:
        return jsonify({"error": f"Неверный формат данных: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)