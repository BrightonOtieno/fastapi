from fastapi import FastAPI
from pydantic import BaseModel
from . import schemas, models
from .database import engine
app = FastAPI()

models.Base.metadata.create_all(engine)
# create a post


@app.post('/blog')
def create_post(request: schemas.Blog):
    return request
