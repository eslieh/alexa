# actions.py
from datetime import datetime
from models import User, Action
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
        return True, username
    else:
        session.close()
        return False, None
