from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str

# create a post


@app.post('/blog')
def create_post(request: Blog):
    return request
