from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

categories_data={
  "Community and Cultural Events": [
    "Festivals",
    "Parades",
    "Community Gatherings"
  ],
  "Recreational and Leisure Events": [
    "Sports Events",
    "Outdoor Activities",
    "Fairs and Carnivals"
  ],
  "Arts and Entertainment": [
    "Concerts and Performances",
    "Film Screenings",
    "Art Exhibits"
  ],
  "Educational and Informative Events": [
    "Workshops and Classes",
    "Seminars and Lectures",
    "Book Fairs and Author Events"
  ],
  "Social and Celebration Events": [
    "Parties",
    "Fundraisers and Charity Events",
    "Holiday Celebrations"
  ],
  "Religious and Spiritual Events": [
    "Religious Services",
    "Spiritual Retreats",
    "Religious Festivals"
  ],
  "Business and Networking Events": [
    "Conferences and Seminars",
    "Networking Events",
    "Product Launches"
  ],
  "Health and Wellness Events": [
    "Health Fairs",
    "Fitness Events",
    "Mental Health Workshops"
  ],
  "Environmental and Sustainability Events": [
    "Clean-Up Drives",
    "Environmental Awareness Events",
    "Gardening and Planting Events"
  ],
  "Youth and Family Events": [
    "Family Fun Days",
    "Youth Sports",
    "Educational Camps"
  ]
}

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    location = Column(String)
    image = Column(String)  # Now stores the URL to the image in S3
    description = Column(Text)

class PostRating(Base):
    __tablename__ = "post_ratings"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    rating = Column(Integer)
    reviewer_user_id = Column(Integer, ForeignKey("users.id"))

class PostComment(Base):
    __tablename__ = "post_comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    comment = Column(Text)
    commenter_user_id = Column(Integer, ForeignKey("users.id"))

class PostLike(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    liked_by_user_id = Column(Integer, ForeignKey("users.id"))

class Event(Base):
    __tablename__= "events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    location = Column(String)
    image = Column(String)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class EventIntrest(Base):
    __tablename__ = "event_intrest"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    intrested_user_id = Column(Integer, ForeignKey("users.id"))
