from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List,Optional,Any

class ResponseModel(BaseModel):
    status_code: int
    msg: str
    data: Optional[Any] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class UserCredentials(BaseModel):
    username: str
    password: str


class PostCreate(BaseModel):
    user_id: int
    location: str
    description: str

class PostRatingCreate(BaseModel):
    post_id: int
    rating: int
    reviewer_user_id: int

class PostCommentCreate(BaseModel):
    post_id: int
    comment: str
    commenter_user_id: int

class PostLikeCreate(BaseModel):
    post_id: int
    liked_by_user_id: int

class PostWithDetails(PostCreate):
    id: int
    likes_count: int
    average_rating: float|None

class EventCreate(BaseModel):
    user_id: int
    category: str
    location: str
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class EventWithDetails(EventCreate):
    id: int

class EventIntrestAdd(BaseModel):
    event_id: int
    intrested_user_id: int