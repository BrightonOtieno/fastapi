from fastapi import APIRouter, Depends, status, Response,HTTPException
from typing import List
from .. import schemas, database, models
from sqlalchemy.orm import Session


router = APIRouter()

get_db = database.get_db

# get all blog posts from db


@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# create post


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    # add the post data into db as a new blog post
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # refresh it so the we can easily return it as feedback
    return new_blog


# DELETE a blog
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==
                                        id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog of id { id } does not exist")

    blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update Blog
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog of id { id } does not exist")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return 'updated'



@ router.get('/blog/{id}', response_model=schemas.ShowBlog, status_code=200, tags=['blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # ERROR 404 (OBJECT DOES NOT EXIST)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} does not exist')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} does not exist'}
    return blog
