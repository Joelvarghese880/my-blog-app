from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey,DateTime
from datetime import datetime, UTC



class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False,index=True)
    email = Column(String(120),unique=True,nullable=False,index=True)
    password = Column(String(255),nullable=False)

    posts = relationship("Post", back_populates="author",cascade="all, delete")

class Post(Base): 
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=UTC))
    author = relationship("User", back_populates="posts")