from database import SessionLocal
from models import User, Resume


db = SessionLocal()

user = User(email="dharani@example.com")

resume = Resume(filename="backend_resume.pdf")

user.resumes.append(resume)

db.add(user)
db.commit()
db.refresh(user)

print("User ID:", user.id)
print("Email:", user.email)
print("Resume ID:", resume.id)
print("Resume User ID:", resume.user_id)

db.close()