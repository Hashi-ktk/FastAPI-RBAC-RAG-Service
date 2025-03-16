# filepath: f:\Upwork Task\test api\fastapi-rbac-microservice\initialize_db.py
from app.database import Base, engine
from app.users.models import User
from app.admin.models import Role

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")