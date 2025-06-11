from sqlmodel import Session, select
from models.order_content import OrderContent

def create_order_content(session: Session, order_content: OrderContent):
    session.add(order_content)
    session.commit()
    session.refresh(order_content)
    return order_content

def get_order_contents(session: Session):
    return session.exec(select(OrderContent)).all()

def get_order_content_by_id(session: Session, order_content_id: int):
    return session.get(OrderContent, order_content_id)

def get_products_by_content_id(session: Session, order_id: int):
    statement = select(OrderContent).where(OrderContent.order_id == order_id)
    orders = session.exec(statement).all()
    products = []
    for order in orders:
        products.append(order.product_id)
    return products

def get_amounts_by_content_id(session: Session, order_id: int):
    statement = select(OrderContent).where(OrderContent.order_id == order_id)
    orders = session.exec(statement).all()
    amounts = []
    for order in orders:
        amounts.append(order.product_amount)
    return amounts

def update_order_content(session: Session, order_content_id: int, order_content_data: dict):
    order_content = session.get(OrderContent, order_content_id)
    if not order_content:
        return None
    for key, value in order_content_data.items():
        setattr(order_content, key, value)
    session.commit()
    session.refresh(order_content)
    return order_content

def delete_order_content(session: Session, order_content_id: int):
    order_content = session.get(OrderContent, order_content_id)
    if order_content:
        session.delete(order_content)
        session.commit()
    return order_content