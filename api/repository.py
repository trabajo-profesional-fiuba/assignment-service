from api.database import TopicPreferences
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.exceptions import TopicPreferencesDuplicated


class Repository:

    def __init__(self, db):
        self._db = db

    def add_topic_preferences(
        self, email: str, topic_preferences: TopicPreferencesItem
    ):
        try:
            db_item = TopicPreferences(
                email=email,
                group_id=topic_preferences.group_id,
                topic1=topic_preferences.topic1,
                topic2=topic_preferences.topic2,
                topic3=topic_preferences.topic3,
            )
            self._db.add(db_item)
            self._db.commit()
            self._db.refresh(db_item)
            return db_item
        except Exception as err:
            self._db.rollback()
            raise TopicPreferencesDuplicated(
                f"Attempt to add a TopicPreferences duplicated for user\
                '{topic_preferences.email}'."
            )
        finally:
            self._db.close()

    def update_topic_preferences(
        self, email: str, topic_preferences_update: TopicPreferencesUpdatedItem
    ):
        try:
            db_item = (
                self._db.query(TopicPreferences)
                .filter(TopicPreferences.email == email)
                .first()
            )

            update_data = topic_preferences_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)

            self._db.commit()
            self._db.refresh(db_item)
            return db_item
        except Exception as err:
            self._db.rollback()
            raise err
        finally:
            self._db.close()
