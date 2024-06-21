from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine, Base, TopicPreferences
from api.models import TopicPreferencesItem

app = FastAPI()


@app.get(
    "/", summary="Root Endpoint", description="This endpoint returns a ping message."
)
async def root():
    return "Ping"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences.",
)
async def add_topic_preferences(
    topic_preferences: TopicPreferencesItem, db: Session = Depends(get_db)
):
    db_item = TopicPreferences(
        email=topic_preferences.email,
        group_id=topic_preferences.group_id,
        topic1=topic_preferences.topic1,
        topic2=topic_preferences.topic2,
        topic3=topic_preferences.topic3,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return topic_preferences
