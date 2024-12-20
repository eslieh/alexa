# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    """User table for storing user details."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, name={self.name})"


class Action(Base):
    """Table to store actions performed by the user."""
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User table
    action_type = Column(String(100), nullable=False)  # e.g., 'login', 'play music'
    action_data = Column(String(255))  # Store extra data, e.g., song name or query
    timestamp = Column(String(50))  # Timestamp of the action

    def __repr__(self):
        return f"Action(id={self.id}, user_id={self.user_id}, action_type={self.action_type}, timestamp={self.timestamp})"

class Contact(Base):
    """Table to store actions performed by the user."""
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # Foreign key to User table
    contact_name = Column(String(255)) 
    phone = Column(String(14)) 
    timestamp = Column(String(50))  # Timestamp of the action

    def __repr__(self): # e.g., 'login', 'play music'
        return f"Action(id={self.id}, user_id={self.user_id}, contact_name={self.contact_name}, phone={self.phone}, timestamp={self.timestamp})"
