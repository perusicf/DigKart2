from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Change user/password if you're using something other than postgres
DATABASE_URL = "postgresql://postgres@localhost:5432/digkar"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
