from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.user import User
from models.order import Order
from models.order_content import OrderContent
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
            order1 = Order(user_id=1)
            order2 = Order(user_id=2)
            order3 = Order(user_id=3)
            order4 = Order(user_id=4)
            session.add_all([order1, order2, order3, order4])
            orderContent1 = OrderContent(order_id=1, product_id=1, product_amount=1)
            orderContent2 = OrderContent(order_id=1, product_id=3, product_amount=2)
            orderContent3 = OrderContent(order_id=1, product_id=4, product_amount=1)
            orderContent4 = OrderContent(order_id=2, product_id=6, product_amount=1)
            orderContent5 = OrderContent(order_id=2, product_id=7, product_amount=1)
            orderContent6 = OrderContent(order_id=3, product_id=11, product_amount=1)
            orderContent7 = OrderContent(order_id=3, product_id=12, product_amount=2)
            orderContent8 = OrderContent(order_id=4, product_id=16, product_amount=6)
            orderContent9 = OrderContent(order_id=4, product_id=17, product_amount=2)
            orderContent10 = OrderContent(order_id=4, product_id=19, product_amount=1)
            orderContent11 = OrderContent(order_id=4, product_id=21, product_amount=3)
            orderContent12 = OrderContent(order_id=4, product_id=23, product_amount=12)
            session.add_all([orderContent1, orderContent2, orderContent3, orderContent4, orderContent5,
                             orderContent6, orderContent7, orderContent8, orderContent9, orderContent10,
                             orderContent11, orderContent12])
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}.")
            
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
