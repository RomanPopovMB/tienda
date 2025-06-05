from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.user import User
from auth.hashing import hash_password

def seed_data():
    drop_db_and_tables() 
    create_db_and_tables()

    with Session(engine) as session:
        try:
            user1 = User(name="client", email="client@email.com", hashed_password=hash_password("123"), role="client")
            user2 = User(name="client2", email="client2@email.com", hashed_password=hash_password("123"), role="client")
            admin1 = User(name="admin", email="admin@email.com", hashed_password=hash_password("123"), role="admin")
            admin2 = User(name="admin2", email="admin2@email.com", hashed_password=hash_password("123"), role="admin")
            session.add_all([user1, user2, admin1, admin2])
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}.")
            
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
