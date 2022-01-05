from fastapi import FastAPI, Depends, status, Response, HTTPException
#from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal, engine
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create post
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    # add the post data into db as a new blog post
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # refresh it so the we can easily return it as feedback
    return new_blog


# DELETE a blog
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update Blog
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update(
        {"title": request.title, "body": request.body})
    db.commit()
    return 'updated'


# get all blog posts from db
@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # ERROR 404 (OBJECT DOES NOT EXIST)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} does not exist')
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} does not exist'}
    return blog
