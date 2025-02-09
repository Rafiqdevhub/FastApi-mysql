from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    username: str

class UserSchema(UserBase):
    id: int  

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model to Pydantic model

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]


@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(user: UserBase, db: db_dependancy):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  
    return db_user  

@app.get('/users/{user_id}', status_code=status.HTTP_200_OK,  response_model=UserSchema)
async def get_user(user_id:int, db:db_dependancy):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@app.post('/posts/', status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase, db:db_dependancy):
    db_post=models.Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(db_post)
    db.commit()
    

@app.get('/posts/', status_code=status.HTTP_200_OK)
async def get_all_posts(db:db_dependancy):
    posts=db.query(models.Post).all()
    return posts

@app.get('/posts/{user_id}', status_code=status.HTTP_200_OK,  response_model=PostBase)
async def get_post(post_id:PostBase, db:db_dependancy):
    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is  None:
        HTTPException(status_code=400, detail="Post not found")
    return post

@app.delete('/posts/{user_id}', status_code=status.HTTP_200_OK)
async def delete_post(Post_id:int, db:db_dependancy):
    db_post=db.query(models.Post).filter(models.Post.id==Post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    