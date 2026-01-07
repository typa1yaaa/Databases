from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Cinema(Base):
    __tablename__ = 'cinema'
    
    cinema_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    city_region = Column(String(100), nullable=False)
    address_cinema = Column(String(100), nullable=False)
    category = Column(String(30))
    total_capacity = Column(Integer, nullable=False)
    
    __table_args__ = (CheckConstraint('total_capacity > 0'), Index('idx_cinema_title', 'title'),)
    
    halls = relationship("CinemaHalls", back_populates="cinema", cascade="all, delete")

class Films(Base):
    __tablename__ = 'films'
    
    film_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    director = Column(String(100), nullable=False)
    operator = Column(String(100))
    main_actors = Column(Text)
    genre = Column(String(30))
    production = Column(String(100))
    session_duration = Column(Integer, nullable=False)
    shot_advertising = Column(String(255))
    
    __table_args__ = (CheckConstraint('session_duration > 0'), Index('idx_films_title', 'title'),)
    
    sessions = relationship("Sessions", back_populates="film", cascade="all, delete")
    prizes = relationship("Prizes", back_populates="film", cascade="all, delete")

class Festival(Base):
    __tablename__ = 'festival'
    
    festival_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    
    __table_args__ = (Index('idx_festival_title', 'title'),)

    prizes = relationship("Prizes", back_populates="festival", cascade="all, delete")

class CinemaHalls(Base):
    __tablename__ = 'cinema_halls'
    
    hall_id = Column(Integer, primary_key=True, autoincrement=True)
    cinema_id = Column(Integer, ForeignKey('cinema.cinema_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    __table_args__ = (CheckConstraint('capacity > 0'),Index('idx_hall_cinemaid', 'cinema_id'),)
    
    cinema = relationship("Cinema", back_populates="halls")
    sessions = relationship("Sessions", back_populates="hall", cascade="all, delete")

class Sessions(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    hall_id = Column(Integer, ForeignKey('cinema_halls.hall_id', ondelete='CASCADE'), nullable=False)
    film_id = Column(Integer, ForeignKey('films.film_id', ondelete='CASCADE'), nullable=False)
    date_session = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    __table_args__ = (Index('idx_sessions_filmid', 'film_id'),)

    hall = relationship("CinemaHalls", back_populates="sessions")
    film = relationship("Films", back_populates="sessions")
    tickets = relationship("Tickets", back_populates="session", cascade="all, delete")

class Tickets(Base):
    __tablename__ = 'tickets'
    
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id', ondelete='CASCADE'), nullable=False)
    row_number = Column(Integer, nullable=False)
    place_number = Column(Integer, nullable=False)
    sold_out = Column(String(1), default='0')
    cost = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('row_number > 0'),
        CheckConstraint('place_number > 0'),
        CheckConstraint('cost >= 0'),
        Index('idx_ticket_sessionid', 'session_id'),
    )
    
    session = relationship("Sessions", back_populates="tickets")

class Prizes(Base):
    __tablename__ = 'prizes'
    
    prizes_id = Column(Integer, primary_key=True, autoincrement=True)
    festival_id = Column(Integer, ForeignKey('festival.festival_id', ondelete='CASCADE'), nullable=False)
    film_id = Column(Integer, ForeignKey('films.film_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    
    __table_args__ = (Index('idx_prizes_filmid', 'film_id'),)

    festival = relationship("Festival", back_populates="prizes")
    film = relationship("Films", back_populates="prizes")