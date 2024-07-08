from pydantic import BaseModel
from datetime import datetime
from typing import List

class PostCreate(BaseModel):
    user_id: int
    timestamp: datetime
    location: str
    image: str  # URL to the image in S3
    description: str

class Post(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    location: str
    image: str  # URL to the image in S3
    description: str

    class Config:
        orm_mode = True

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

class PostWithDetails(Post):
    likes_count: int
    average_rating: float|None
