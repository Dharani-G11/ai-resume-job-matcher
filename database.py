import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase , sessionmaker
from sqlalchemy.engine import URL

load_dotenv()
class Base (DeclarativeBase):
    pass




database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USERNAME", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "host.docker.internal"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "ai_resume_matcher")
)

engine = create_engine(database_url)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)