from sqlalchemy.orm import Session
from src.api.form.schemas import GroupFormRequest
from src.api.form.models import GroupFormSubmittion
from src.api.topic.models import Topic, TopicCategory


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group_form(self, group_form: GroupFormRequest):
        try:
            with self.Session() as session:
                topics = session.query(Topic).fiter(
                    (Topic.name == group_form.topic_1)
                    | (Topic.name == group_form.topic_2)
                    | (Topic.name == group_form.topic_3)
                )
                uids = (
                    group_form.uid_sender,
                    group_form.uid_student_2,
                    group_form.uid_student_3,
                    group_form.uid_student_4,
                )

                if len(topics) == 3:
                    db_items = []
                    for uid in uids:
                        if uid is not None:
                            db_item = GroupFormSubmittion(
                                uid=uid,
                                group_id=group_form.group_id,
                                topic_1=group_form.topic_1,
                                topic_2=group_form.topic_2,
                                topic_3=group_form.topic_3,
                            )
                    session.add(db_item)
                    session.commit()
                    return db_item
        except Exception as err:
            session.rollback()
            raise err
