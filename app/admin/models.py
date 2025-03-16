from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("AdminUser", back_populates="role")

class AdminUser(Base):  # Renamed to avoid confusion with the User model
    __tablename__ = 'admin_users'  # Ensure this table name is unique

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="users")