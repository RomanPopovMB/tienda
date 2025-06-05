from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    name: str = Field(index=True, unique=True)
    role: str = Field(default="client")
    email: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    refresh_token: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
