from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./app/data.db"

engine = create_engine(
    SQLITE_DATABASE_URL, 
    echo = True,
    connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()