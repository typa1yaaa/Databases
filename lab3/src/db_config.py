from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:000000@localhost:5432/lb3"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()
