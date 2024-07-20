from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, database
from app.models import Base,categories_data
from app.crud import (login_user, create_user, create_post, get_posts, rate_post, comment_post,like_post,uncomment_post,unlike_post,edit_rating_post,remove_post,
                      get_liked_by_users,get_post_comments,get_rated_by_users,create_event, get_events, get_intrested_users, add_intrest, remove_intrest,follow_user,
                      unfollow_user, get_followers, get_following, get_user_profile)
from app.s3 import get_presigned_url_post,get_presigned_url_get
from app.schemas import ResponseModel,PostCreate, PostRatingCreate, PostCommentCreate, PostLikeCreate, EventCreate, EventIntrestAdd, UserCreate, UserCredentials
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"status_code":422,"msg":"validation error","data": [str(i["loc"][1])+":"+i["msg"] for i in exc.errors()]})

@app.post("/register", response_model=ResponseModel, status_code=201)
async def register_user_endpoint(user: UserCreate):
    return await create_user(user)

@app.post("/login", response_model=ResponseModel, status_code=201)
async def login_user_endpoint(credentials: UserCredentials):
    return await login_user(credentials)

@app.post("/posts", response_model=ResponseModel, status_code=201)
async def create_post_endpoint(post: PostCreate):
    return await create_post(post)

@app.get("/posts", response_model=ResponseModel, status_code=200)
async def get_posts_endpoint(location: str, skip: int = 0, limit: int = 10):
    return await get_posts(location, skip, limit)

@app.post("/posts/{post_id}/rating", response_model=ResponseModel, status_code=201)
async def rate_post_endpoint(post_id: int, rating: PostRatingCreate):
    rating.post_id = post_id
    return await rate_post(rating)

@app.post("/posts/{post_id}/comment", response_model=ResponseModel, status_code=201)
async def comment_post_endpoint(post_id: int, comment: PostCommentCreate):
    comment.post_id = post_id
    return await comment_post(comment)

@app.post("/posts/{post_id}/like", response_model=ResponseModel, status_code=201)
async def like_post_endpoint(post_id: int, like: PostLikeCreate):
    like.post_id = post_id
    return await like_post(like)

@app.delete("/posts/{post_id}/like", response_model=ResponseModel, status_code=200)
async def unlike_post_endpoint(post_id: int, user_id: int):
    return await unlike_post(post_id, user_id)

@app.delete("/posts/comment/{comment_id}", response_model=ResponseModel, status_code=200)
async def uncomment_post_endpoint(comment_id: int, user_id: int):
    return await uncomment_post(comment_id, user_id)

@app.put("/posts/rating/{rating_id}", response_model=ResponseModel, status_code=200)
async def edit_rating_post_endpoint(rating_id: int, new_rating: int, user_id: int):
    return await edit_rating_post(rating_id, new_rating, user_id)

@app.delete("/posts/{post_id}", response_model=ResponseModel, status_code=200)
async def remove_post_endpoint(post_id: int, user_id: int):
    return await remove_post(post_id, user_id)

@app.get("/posts/{post_id}/likes", response_model=ResponseModel, status_code=200)
async def get_liked_by_users_endpoint(post_id: int):
    return await get_liked_by_users(post_id)

@app.get("/posts/{post_id}/ratings", response_model=ResponseModel, status_code=200)
async def get_rated_by_users_endpoint(post_id: int):
    return await get_rated_by_users(post_id)

@app.get("/posts/{post_id}/comments", response_model=ResponseModel, status_code=200)
async def get_post_comments_endpoint(post_id: int):
    return await get_post_comments(post_id)

@app.get("/events/categories")
async def get_event_categories():
    return  ResponseModel(status_code=200,msg="categories returned successfully",data=categories_data)

@app.post("/events", response_model=ResponseModel, status_code=201)
async def create_events_endpoint(event: EventCreate):
    return await create_event(event)

@app.get("/events", response_model=ResponseModel, status_code=200)
async def get_events_endpoint(location: str, skip: int = 0, limit: int = 10):
    return await get_events(location, skip, limit)

@app.post("/events/{event_id}/intrest", response_model=ResponseModel, status_code=201)
async def add_intrest_endpoint(event_id: int, intrest: EventIntrestAdd):
    intrest.event_id = event_id
    return await add_intrest(intrest)

@app.delete("/events/{event_id}/intrest", response_model=ResponseModel, status_code=200)
async def remove_intrest_endpoint(event_id: int, user_id: int):
    return await remove_intrest(event_id, user_id)

@app.get("/events/{event_id}/intrested_users", response_model=ResponseModel, status_code=200)
async def get_intrested_users_endpoint(event_id: int):
    return await get_intrested_users(event_id)

@app.post("/users/{user_id}/follow", response_model=ResponseModel, status_code=201)
async def follow_user_endpoint(user_id: int, followed_id: int):
    return await follow_user(user_id, followed_id)

@app.delete("/users/{user_id}/unfollow/{followed_id}", response_model=ResponseModel, status_code=200)
async def unfollow_user_endpoint(user_id: int, followed_id: int):
    return await unfollow_user(user_id, followed_id)

@app.get("/users/{user_id}/followers", response_model=ResponseModel, status_code=200)
async def get_followers_endpoint(user_id: int):
    return await get_followers(user_id)

@app.get("/users/{user_id}/following", response_model=ResponseModel, status_code=200)
async def get_following_endpoint(user_id: int):
    return await get_following(user_id)

@app.get("/users/{user_id}/profile", response_model=ResponseModel, status_code=200)
async def get_user_profile_endpoint(user_id: int):
    return await get_user_profile(user_id)

@app.get("/s3_upload_url/{folder}/{id}", status_code=200)               #folder=profile_pics , id=user_id and folder=posts , id=post_id
async def s3_upload_url_endpoint(folder: str, id: int):
    key= folder + "/" + str(id)
    return get_presigned_url_post(key)

@app.get("/s3_get_url/{folder}/{id}", status_code=200)                
async def s3_get_url_endpoint(folder: str, id: int):
    key= folder + "/" + str(id)
    return get_presigned_url_get(key)