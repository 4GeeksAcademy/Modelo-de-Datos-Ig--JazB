import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Enum as SQLEnum
from enum import Enum
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()


# USUARIOS


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    posts = relationship("Post", backref="author",
                         lazy=True, cascade="all, delete-orphan")
    comments = relationship("Comment", backref="author",
                            lazy=True, cascade="all, delete-orphan")
    likes = relationship("Like", backref="user", lazy=True,
                         cascade="all, delete-orphan")


# RELACIÓN FOLLOWERS
class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        "follower_id", "followed_id", name="unique_follow"),)


# POSTS
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    caption = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relaciones
    media = relationship("Media", backref="post", lazy=True,
                         cascade="all, delete-orphan")
    comments = relationship("Comment", backref="post",
                            lazy=True, cascade="all, delete-orphan")
    likes = relationship("Like", backref="post", lazy=True,
                         cascade="all, delete-orphan")


# TIPOS DE MEDIA
class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


# MEDIA
class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    type = Column(SQLEnum(MediaType), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)


# COMENTARIOS
class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)


# LIKES
class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        "user_id", "post_id", name="unique_like"),)


# GENERAR DIAGRAMA

def to_dict(self):
    return {}


render_er(Base, "diagram.png")

