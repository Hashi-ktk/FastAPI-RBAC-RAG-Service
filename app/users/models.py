from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Integer, String, Boolean, event
from app.database import Base
from app.admin.models import Role, AdminUser  # Import AdminUser model

class User(Base):
    __tablename__ = 'users'  # Ensure this table name is unique

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

# Add this function to query the user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

@event.listens_for(User, "after_insert")
def handle_admin_user_creation(mapper, connection, target):
    session = Session(bind=connection)
    try:
        if target.is_admin:
            # Ensure the "Admin" role exists in the roles table
            admin_role = session.query(Role).filter(Role.name == "Admin").first()
            if not admin_role:
                admin_role = Role(name="Admin", description="Administrator role")
                session.add(admin_role)

            # Create an entry in the admin_users table
            existing_admin_user = session.query(AdminUser).filter(AdminUser.username == target.username).first()
            if not existing_admin_user:
                admin_user = AdminUser(
                    username=target.username,
                    password_hash=target.hashed_password,
                    role_id=admin_role.id if admin_role else None  # Assign the Admin role ID
                )
                session.add(admin_user)

        else:
            # Ensure the "User" role exists in the roles table
            user_role = session.query(Role).filter(Role.name == "User").first()
            if not user_role:
                user_role = Role(name="User", description="Regular user role")
                session.add(user_role)

        session.commit()
    finally:
        session.close()