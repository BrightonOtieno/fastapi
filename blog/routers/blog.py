from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

get_db = database.get_db

# get all blog posts from db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


# DELETE a blog
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, responses={204: {"model": None}})
def destroy(id, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


# update Blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@ router.get('/{id}', response_model=schemas.ShowBlog, status_code=200)
def show(id:int, response: Response, db: Session = Depends(get_db)):
    return blog.show(id, db)
