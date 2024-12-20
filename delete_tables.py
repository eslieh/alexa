from sqlalchemy.orm import Session
from models import User, Action, Contact
from database import engine

def delete_all_records():
    """Delete all records from User, Action, and Contact tables."""
    with Session(engine) as session:
        try:
            # Ask for user confirmation
            confirmation = input("Are you sure you want to delete all records? This action cannot be undone. (yes/no): ").strip().lower()
            if confirmation != 'yes':
                print("Operation canceled.")
                return
            
            # Delete all records from each table
            session.query(User).delete()
            session.query(Action).delete()
            session.query(Contact).delete()
            session.commit()
            print("All records deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred while deleting records: {e}")

if __name__ == '__main__':
    delete_all_records()
