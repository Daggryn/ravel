from app.database import SessionLocal
from app import models
from app.auth import hash_password
import os
from dotenv import load_dotenv

load_dotenv()


def seed_users():
    db = SessionLocal()

    existing = db.query(models.User).count()
    if existing > 0:
        print("Users already seeded, skipping.")
        db.close()
        return

    users = [
        models.User(
            username="josh",
            hashed_password=hash_password(os.getenv("JOSH_PASSWORD",""))
        ),
        models.User(
            username="estelle",
            hashed_password=hash_password(os.getenv("ESTELLE_PASSWORD",""))
        ),
    ]

    db.add_all(users)
    db.commit()
    db.close()
    print("Users seeded.")
