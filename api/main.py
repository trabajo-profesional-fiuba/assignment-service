from fastapi import FastAPI, HTTPException
from api.repository import Repository
from api.service import Service
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.database import Database
from api.exceptions import TopicPreferencesDuplicated
from api.controller import Controller

app = FastAPI()
database = Database()
session = database.setup()
repository = Repository(session)
service = Service(repository)
controller = Controller(service)


@app.get("/", description="This endpoint returns a ping message.")
async def root():
    return "Ping"


@app.post(
    "/topic_preferences/",
    status_code=201,
    description="This endpoint creates a new topic preferences.",
)
async def add_topic_preferences(topic_preferences: TopicPreferencesItem):
    try:
        new_item = controller.add_topic_preferences(topic_preferences)
        return new_item
    except TopicPreferencesDuplicated:
        raise HTTPException(status_code=409, detail="Topic preference already exists.")
    except Exception as err:
        raise err


@app.put(
    "/topic_preferences/{email}",
    status_code=200,
    description="Update an existing topic preferences.",
)
async def update_topic_preferences(
    email: str,
    topic_preferences_update: TopicPreferencesUpdatedItem,
):
    try:
        updated_items = controller.update_topic_preferences(
            email, topic_preferences_update
        )
        return updated_items
    except Exception as err:
        raise err
