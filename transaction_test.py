from database import SessionLocal
from models import User


db = SessionLocal()

try:
    user = User(email="rollback_test@example.com")

    db.add(user)

    # Force an error before commit
    raise Exception("Something went wrong")

    db.commit()

except Exception as e:
    db.rollback()
    print("Transaction rolled back")
    print("Error:", e)

finally:
    db.close()