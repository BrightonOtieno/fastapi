from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from .. oauth2 import get_current_user
from ..repository import user

get_db = database.get_db

router = APIRouter(
    prefix='/user',
    tags=['users']
)


# CREATE USER
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.create_user(request, db)


# GET User
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get_user(id, db)
