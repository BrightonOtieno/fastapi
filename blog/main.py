from fastapi import FastAPI
from pydantic import BaseModel
from . import schemas

app = FastAPI()


# create a post


@app.post('/blog')
def create_post(request: schemas.Blog):
    return request
