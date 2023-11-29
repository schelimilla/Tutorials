# main file for fastAPI app

from fastapi import FastAPI, HTTPException, Depends, status, Response
from pydantic import BaseModel #data validation
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.sql import text

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

def validate(arg):
    if arg == 2:
        raise HTTPException(status_code=418, detail="This is a custom message")
    

def generate_error_messages():
    # raise HTTPException(status_code=200)
    raise HTTPException(status_code=201)
    raise HTTPException(status_code=202)
    raise HTTPException(status_code=203)
    raise HTTPException(status_code=204)
    raise HTTPException(status_code=205)


def display_error_messages():
    # error_codes_messages = {"200":"OK", "201":"created"}
    # return error_codes_messages
    errors = [204, 205, 206, 207]
    # x = HTTPException(status_code=204)
    # y = HTTPException(status_code=205)
    l = []
    for error_code in errors:
        x = HTTPException(status_code=error_code)
        l.append(x)
    
    return l


# instantiate app
app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

models.Base.metadata.create_all(bind=engine) #creates tables in MySQL database based on the definitions in model.py

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] #db and class

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db:db_dependency):
    # db_post = models.Post(**post.model_dump())
    post = post.model_dump()
    # db.add(db_post)
    # db.commit()
    statement = text("INSERT INTO posts(title, content, user_id) VALUES(:title, :content, :user_id)")
    db.execute(statement, post)
    db.commit()

@app.get("/posts/", status_code=status.HTTP_200_OK)
async def get_all_posts(db:db_dependency):
    statement = text("SELECT * FROM posts")
    result = db.execute(statement)
    post = result.fetchall()
    all_posts = []
    for i in range(len(post)):
        post_dict = {'id':post[i][0], 'title':post[i][1], 'content':post[i][2], 'user_id':post[i][3]}
        all_posts.append(post_dict)
    return all_posts

@app.post("/posts/display_api_error_codes/")
async def display_errors():
    error_messages = display_error_messages()
    return error_messages
   
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id:int, db:db_dependency):
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()
    # if post is None:
    #     raise HTTPException(status_code=404, detail='Post was not found')
    # return post

    # if type(post_id) is not int:
    #     raise HTTPException(status_code=418, detail="This is a custom message")

    # if post_id == 2:
    #     raise HTTPException(status_code=418, detail="This is a custom message")
    validate(2)
    statement = text("SELECT * FROM posts WHERE posts.id = :post_id")
    result = db.execute(statement, {'post_id': post_id})
    post = result.fetchall()
    post_dict = {'id':post[0][0], 'title':post[0][1], 'content':post[0][2], 'user_id':post[0][3]}
    return post_dict
   
@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db:db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump()) #get all data and de-serialize it into user object
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id:int, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first() #return first entry in db that matches this filter
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user
