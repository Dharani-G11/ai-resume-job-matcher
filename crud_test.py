from database import SessionLocal
from models import Resume


db = SessionLocal()

resume = db.query(Resume).filter(Resume.id == 1).first()

db.delete(resume)
db.commit()

print("Resume deleted")

db.close()