from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


print("DB TEST STARTED")


database_url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="dharani@11",
    host="localhost",
    port=5432,
    database="ai_resume_matcher"
)


print("URL CREATED")


engine = create_engine(database_url)

print("ENGINE CREATED")


with engine.connect() as connection:
    print("CONNECTED")

    result = connection.execute(text("SELECT 1"))

    print("QUERY EXECUTED")

    print(result.scalar())