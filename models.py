from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True,index=True)
    
class Post(Base):
    __tablename__='posts'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(500),index=True)
    content=Column(String(500))
    user_id=Column(Integer)