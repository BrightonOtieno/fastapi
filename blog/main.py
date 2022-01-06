from typing import List

from sqlalchemy.sql.functions import user
from fastapi import FastAPI, Depends, status, Response, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal, engine, get_db
from .routers import blog, user


app = FastAPI()

models.Base.metadata.create_all(engine) 

app.include_router(blog.router)
app.include_router(user.router)



