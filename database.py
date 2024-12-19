# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URI for SQLite (can be modified for other databases)
DATABASE_URI = 'sqlite:///database/user_data.db'

# Set up the database connection
engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
Base = declarative_base()

# Set up sessionmaker for creating database sessions
Session = sessionmaker(bind=engine)
