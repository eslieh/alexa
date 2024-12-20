# actions.py
from datetime import datetime
from models import User, Action, Contact
from database import Session

def log_action(user_id, action_type, action_data=""):
    """Log an action performed by the user."""
    session = Session()
    new_action = Action(
        user_id=user_id,
        action_type=action_type,
        action_data=action_data,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    session.add(new_action)
    session.commit()
    session.close()


def signup(username, password, name):
    """Signup logic."""
    from werkzeug.security import generate_password_hash

    session = Session()
    hashed_password = generate_password_hash(password)
    try:
        new_user = User(username=username, password=hashed_password, name=name)
        session.add(new_user)
        session.commit()
        user_id = new_user.id
        log_action(user_id, 'signup')
        session.close()
        return True, user_id
    except Exception as e:
        session.rollback()
        session.close()
        print(f"Error: {e}")
        return False, None


def login(username, password):
    """Login logic."""
    from werkzeug.security import check_password_hash

    session = Session()
    user = session.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        user_id = user.id
        username = user.name
        log_action(user_id, 'login')
        session.close()
        return True, username, user_id
    else:
        session.close()
        return False, None
    
def get_user_id_by_username(username):
    """Fetch the user_id from the User table based on the username."""
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user.id if user else None

def add_contact(user_id, name, phone):
    """Add contact."""
    session = Session()
    # Check if the contact already exists
    existing_contact = session.query(Contact).filter(Contact.user_id == user_id, Contact.contact_name == name).first()
    if existing_contact:
        session.close()
        return f"Contact {name} already exists for user {user_id}."

    # Add the new contact
    new_contact = Contact(
        user_id=user_id,
        contact_name=name,
        phone=phone,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    session.add(new_contact)
    session.commit()
    session.close()
    return f"Contact {name} added successfully for user {user_id}."

def get_contact(user_id, name):
    """Get contact."""
    session = Session()
    if not user_id:
        session.close()
        return False, f"User with username {user_id} does not exist."

    # Query the contact
    contact = session.query(Contact).filter(Contact.contact_name == name, Contact.user_id == user_id).first()
    if contact:
        phone_number = contact.phone
        session.close()
        return True, phone_number
    else:
        session.close()
        return False, None


    