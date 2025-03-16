from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.users.models import User as UserModel
from app.auth.utils import hash_password

def create_admin_user():
    # Database session
    db: Session = SessionLocal()

    try:
        # Check if the admin user already exists
        existing_user = db.query(UserModel).filter(UserModel.username == "admin").first()
        if existing_user:
            print("Admin user already exists.")
            return

        # Create a new admin user
        admin_user = UserModel(
            username="admin",
            email="admin@gmail.com",
            hashed_password=hash_password("admin"),  # Hash the password
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()