from sqlalchemy import select, func
from app.models import Post, PostRating, PostComment, PostLike, Event, EventIntrest
from app.schemas import ResponseModel,PostCreate, PostRatingCreate, PostCommentCreate, PostLikeCreate, PostWithDetails, EventCreate, EventWithDetails, EventIntrestAdd
from app.database import database
from fastapi import HTTPException
from sqlalchemy import delete, update

#create post
async def create_post(post: PostCreate):
    try:
        query = Post.__table__.insert().values(
            user_id=post.user_id,
            timestamp=post.timestamp,
            location=post.location,
            image=post.image,
            description=post.description,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="Post created successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

#fetch posts
async def get_posts(location: str, skip: int = 0, limit: int = 10):
    try:
        query = select(
            Post,
            func.count(PostLike.id).label('likes_count'),
            func.avg(PostRating.rating).label('average_rating')
        ).outerjoin(PostLike, Post.id == PostLike.post_id
        ).outerjoin(PostRating, Post.id == PostRating.post_id
        ).where(Post.location == location
        ).group_by(Post.id
        ).offset(skip).limit(limit)
        results = await database.fetch_all(query)
        return ResponseModel(status_code=201,msg="fetched successfully",data=[PostWithDetails(**dict(result)) for result in results])
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    
#rate a post
async def rate_post(rating: PostRatingCreate):
    try:
        query = PostRating.__table__.insert().values(
            post_id=rating.post_id,
            rating=rating.rating,
            reviewer_user_id=rating.reviewer_user_id,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="rated successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

async def comment_post(comment: PostCommentCreate):
    try:
        query = PostComment.__table__.insert().values(
            post_id=comment.post_id,
            comment=comment.comment,
            commenter_user_id=comment.commenter_user_id,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="comment added successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

async def like_post(like: PostLikeCreate):
    try:
        query = PostLike.__table__.insert().values(
            post_id=like.post_id,
            liked_by_user_id=like.liked_by_user_id,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="like added successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    

# Unlike a post
async def unlike_post(post_id: int, user_id: int):
    try:
        query = delete(PostLike).where(PostLike.post_id == post_id, PostLike.liked_by_user_id == user_id)
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="like removed successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

# Uncomment a post
async def uncomment_post(comment_id: int, user_id: int):
    try:
        query = delete(PostComment).where(PostComment.id == comment_id, PostComment.commenter_user_id == user_id)
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="comment removed successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

# Edit rating
async def edit_rating_post(rating_id: int, new_rating: int, user_id: int):
    try:
        query = update(PostRating).where(PostRating.id == rating_id, PostRating.reviewer_user_id == user_id).values(rating=new_rating)
        data=await database.execute(query)
        return ResponseModel(status_code=201,msg="rating updated successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    
#delete post
async def remove_post(post_id: int, user_id: int):
    try:
        # Assuming only the user who created the post can delete it
        query = delete(Post).where(Post.id == post_id, Post.user_id == user_id)
        data=await database.execute(query)
        return ResponseModel(status_code=200,msg="post deleted successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

# Get users who liked a post
async def get_liked_by_users(post_id: int):
    try:
        query = select(PostLike.liked_by_user_id).where(PostLike.post_id == post_id)
        results = await database.fetch_all(query)
        return [result["liked_by_user_id"] for result in results]
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

# Get users who rated a post
async def get_rated_by_users(post_id: int):
    try:
        query = select(PostRating.reviewer_user_id).where(PostRating.post_id == post_id)
        results = await database.fetch_all(query)
        return ResponseModel(status_code=200,msg="fetched successfully",data=[result["reviewer_user_id"] for result in results])
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

# Get comments for a post
async def get_post_comments(post_id: int):
    try:
        query = select(PostComment).where(PostComment.post_id == post_id)
        results = await database.fetch_all(query)
        return ResponseModel(status_code=200,msg="fetched comments successfully",data=[dict(result) for result in results])
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

#create event
async def create_event(event: EventCreate):
    try:
        query = Event.__table__.insert().values(
            user_id=event.user_id,
            title=event.title,
            category=event.category,
            location=event.location,
            image=event.image,
            description=event.description,
            start_time=event.start_time,
            end_time=event.end_time,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=200,msg="event created successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    
#fetch events
async def get_events(location: str, skip: int = 0, limit: int = 10):
    try:
        query = select(
            Event
        ).where(Event.location == location
        ).offset(skip).limit(limit)
        results = await database.fetch_all(query)
        return ResponseModel(status_code=200,msg="fetched events successfully",data=[EventWithDetails(**dict(result)) for result in results])
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    
async def add_intrest(intrest: EventIntrestAdd):
    try:
        query = EventIntrest.__table__.insert().values(
            event_id=intrest.event_id,
            intrested_user_id=intrest.intrested_user_id,
        )
        data=await database.execute(query)
        return ResponseModel(status_code=200,msg="intrest added successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))

async def remove_intrest(event_id: int, user_id: int):
    try:
        query = delete(EventIntrest).where(EventIntrest.event_id == event_id, EventIntrest.intrested_user_id == user_id)
        data=await database.execute(query)
        return ResponseModel(status_code=200,msg="intrest removed successfully",data=data)
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))
    
# Get users who are intrested in a event
async def get_intrested_users(event_id: int):
    try:
        query = select(EventIntrest.intrested_user_id).where(EventIntrest.event_id == event_id)
        results = await database.fetch_all(query)
        return ResponseModel(status_code=200,msg="fetched successfully",data=[result["intrested_user_id"] for result in results])
    except Exception as e:
        return ResponseModel(status_code=500,msg="DataBase Error",data=str(e))