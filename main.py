# main file for fastAPI app

from fastapi import FastAPI, HTTPException, Depends, status, Response
from pydantic import BaseModel #data validation
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from sqlalchemy.sql import text


# instantiate app
app = FastAPI()
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

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id:int, db:db_dependency):
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()
    # if post is None:
    #     raise HTTPException(status_code=404, detail='Post was not found')
    # return post
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