from blog.database import Base
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    author: ShowUser

    class Config():
        orm_mode = True


class Blog(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True
