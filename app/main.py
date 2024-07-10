from fastapi import FastAPI, File, UploadFile,Form
from app.database import engine, database
from app.models import Base,categories_data
from app.crud import create_post, get_posts, rate_post, comment_post,like_post,uncomment_post,unlike_post,edit_rating_post,remove_post,get_liked_by_users,get_post_comments,get_rated_by_users,create_event, get_events, get_intrested_users, add_intrest, remove_intrest
from app.schemas import PostCreate, PostRatingCreate, PostCommentCreate, PostLikeCreate, PostWithDetails, EventCreate, EventWithDetails, EventIntrestAdd
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/posts", status_code=201)
async def create_post_endpoint(user_id: int = Form(...), timestamp: datetime = Form(...), location: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    #image_url = await upload_image_to_s3(file)
    post = PostCreate(user_id=user_id, timestamp=timestamp, location=location, image="image_url", description=description)
    return await create_post(post)

@app.get("/posts", response_model=list[PostWithDetails], status_code=200)
async def get_posts_endpoint(location: str, skip: int = 0, limit: int = 10):
    return await get_posts(location, skip, limit)

@app.post("/posts/{post_id}/rating", status_code=201)
async def rate_post_endpoint(post_id: int, rating: PostRatingCreate):
    rating.post_id = post_id
    return await rate_post(rating)

@app.post("/posts/{post_id}/comment", status_code=201)
async def comment_post_endpoint(post_id: int, comment: PostCommentCreate):
    comment.post_id = post_id
    return await comment_post(comment)

@app.post("/posts/{post_id}/like", status_code=201)
async def like_post_endpoint(post_id: int, like: PostLikeCreate):
    like.post_id = post_id
    return await like_post(like)

@app.delete("/posts/{post_id}/like", status_code=200)
async def unlike_post_endpoint(post_id: int, user_id: int):
    return await unlike_post(post_id, user_id)

@app.delete("/posts/comment/{comment_id}", status_code=200)
async def uncomment_post_endpoint(comment_id: int, user_id: int):
    return await uncomment_post(comment_id, user_id)

@app.put("/posts/rating/{rating_id}", status_code=200)
async def edit_rating_post_endpoint(rating_id: int, new_rating: int, user_id: int):
    return await edit_rating_post(rating_id, new_rating, user_id)

@app.delete("/posts/{post_id}", status_code=200)
async def remove_post_endpoint(post_id: int, user_id: int):
    return await remove_post(post_id, user_id)

@app.get("/posts/{post_id}/likes", status_code=200)
async def get_liked_by_users_endpoint(post_id: int):
    return await get_liked_by_users(post_id)

@app.get("/posts/{post_id}/ratings", status_code=200)
async def get_rated_by_users_endpoint(post_id: int):
    return await get_rated_by_users(post_id)

@app.get("/posts/{post_id}/comments", status_code=200)
async def get_post_comments_endpoint(post_id: int):
    return await get_post_comments(post_id)

@app.get("/events/categories")
async def get_event_categories():
    return categories_data

@app.post("/events", status_code=201)
async def create_events_endpoint(user_id: int = Form(...),category: str = Form(...), start_time: datetime = Form(...),end_time:datetime = Form(...),title: str = Form(...), location: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    #image_url = await upload_image_to_s3(file)
    event = EventCreate(user_id=user_id,category=category, start_time=start_time, end_time=end_time,title=title, location=location, image="image_url", description=description)
    return await create_event(event)


@app.get("/events", response_model=list[EventWithDetails], status_code=200)
async def get_events_endpoint(location: str, skip: int = 0, limit: int = 10):
    return await get_events(location, skip, limit)

@app.post("/events/{event_id}/intrest", status_code=201)
async def add_intrest_endpoint(event_id: int, intrest: EventIntrestAdd):
    intrest.event_id = event_id
    return await add_intrest(intrest)

@app.delete("/events/{event_id}/intrest", status_code=200)
async def remove_intrest_endpoint(event_id: int, user_id: int):
    return await remove_intrest(event_id, user_id)

@app.get("/events/{event_id}/intrested_users", status_code=200)
async def get_intrested_users_endpoint(event_id: int):
    return await get_intrested_users(event_id)