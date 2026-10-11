from database import engine, Base
from models import Resume

Base.metadata.create_all(engine)

print("Tables created")