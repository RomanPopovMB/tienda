from sqlmodel import SQLModel, Field
from typing import Optional

class OrderContentBase(SQLModel):
    order_id: int
    product_id: int
    product_amount: int

class OrderContent(OrderContentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class OrderContentCreate(OrderContentBase):
    pass

class OrderContentRead(OrderContentBase):
    id: int