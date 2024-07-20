from sqlalchemy.orm import Session
from src.api.form.schemas import GroupFormRequest, GroupFormResponse
from src.api.form.models import GroupFormPreferences
from src.api.topic.models import Topic, TopicCategory


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group_form(self, group_form: GroupFormRequest, uids: list[int]):
        try:
            with self.Session() as session:
                topics = (
                    session.query(Topic)
                    .filter(
                        (Topic.name == group_form.topic_1)
                        | (Topic.name == group_form.topic_2)
                        | (Topic.name == group_form.topic_3)
                    )
                    .all()
                )
                db_items = []
                responses = []
                for uid in uids:
                    db_item = GroupFormPreferences(
                        uid=uid,
                        group_id=group_form.group_id,
                        topic_1=group_form.topic_1,
                        topic_2=group_form.topic_2,
                        topic_3=group_form.topic_3,
                    )
                    db_items.append(db_item)
                    responses.append(GroupFormResponse.from_orm(db_item))
                session.add_all(db_items)
                session.commit()
                return responses
        except Exception as err:
            session.rollback()
            raise err
