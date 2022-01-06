from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal, engine, get_db
from .routers import blog


app = FastAPI()

models.Base.metadata.create_all(engine) 

app.include_router(blog.router)


# password hashing context
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""







# CREATE USER
@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET User
@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    return user
