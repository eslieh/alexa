# create_tables.py
from models import User, Action, Contact
from database import engine

# Create all tables in the database
User.metadata.create_all(engine)
Action.metadata.create_all(engine)
Contact.metadata.create_all(engine)

print("Tables created successfully.")
