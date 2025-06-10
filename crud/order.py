from sqlmodel import Session, select
from models.order import Order

def create_order(session: Session, order: Order):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_orders(session: Session):
    return session.exec(select(Order)).all()

def get_order_by_id(session: Session, order_id: int):
    return session.get(Order, order_id)

def update_order(session: Session, order_id: int, order_data: dict):
    order = session.get(Order, order_id)
    if not order:
        return None
    for key, value in order_data.items():
        setattr(order, key, value)
    session.commit()
    session.refresh(order)
    return order

def delete_order(session: Session, order_id: int):
    order = session.get(Order, order_id)
    if order:
        session.delete(order)
        session.commit()
    return order