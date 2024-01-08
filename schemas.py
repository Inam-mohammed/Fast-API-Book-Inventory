from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_admin: Optional[bool] = False


class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    name: str
    email: str
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    message: str
    user_details: User
    status: int


class BookBase(BaseModel):
    title: str
    description: str
    author: str
    count: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookResponse(BookBase):
    message: str
    book: BookBase
    status: int


class CategoryResponse(BaseModel):
    title: str