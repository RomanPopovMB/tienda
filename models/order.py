from sqlmodel import SQLModel, Field
from typing import Optional

class OrderBase(SQLModel):
    user_id: int

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int