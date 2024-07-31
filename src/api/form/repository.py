from sqlalchemy import exc
from sqlalchemy.orm import Session
from datetime import datetime

from src.api.form.schemas import GroupFormRequest, GroupFormResponse
from src.api.form.models import GroupFormPreferences
from src.api.form.exceptions import StudentNotFound
from src.api.users.model import User, Role
from src.api.topic.models import Topic
from src.api.form.exceptions import TopicNotFound, DuplicatedAnswer


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _verify_topics(self, session, topics: list[str]):
        for topic in topics:
            if not session.query(Topic).filter_by(name=topic).first():
                raise TopicNotFound(f"Topic '{topic}' not found.")

    def _verify_user(self, session, uid: int):
        user = session.query(User).filter_by(id=uid).first()
        if not user:
            raise StudentNotFound(f"Student with uid '{uid}' not found.")
        if user.rol != Role.STUDENT:
            raise StudentNotFound("The student must have the role 'student'.")

    def _verify_answer(self, session, group_form: GroupFormRequest, uids: list[int]):
        count = 0
        for uid in uids:
            answer = (
                session.query(GroupFormPreferences)
                .filter_by(
                    uid=uid,
                    topic_1=group_form.topic_1,
                    topic_2=group_form.topic_2,
                    topic_3=group_form.topic_3,
                )
                .first()
            )
            if answer is not None:
                count += 1
        if count == len(uids):
            raise DuplicatedAnswer("The answer already exists.")

    def add_group_form(self, group_form: GroupFormRequest, uids: list[int]):
        with self.Session() as session:
            with session.begin():
                db_items = []
                responses = []
                self._verify_topics(
                    session,
                    [group_form.topic_1, group_form.topic_2, group_form.topic_3],
                )
                self._verify_answer(session, group_form, uids)
                for uid in uids:
                    self._verify_user(session, uid)
                    db_item = GroupFormPreferences(
                        uid=uid,
                        group_id=group_form.group_id,
                        topic_1=group_form.topic_1,
                        topic_2=group_form.topic_2,
                        topic_3=group_form.topic_3,
                    )
                    db_items.append(db_item)
                    responses.append(GroupFormResponse.model_validate(db_item))
                session.add_all(db_items)
                return responses

    def delete_group_form_by_group_id(self, group_id: datetime):
        with self.Session() as session:
            with session.begin():
                session.query(GroupFormPreferences).filter_by(
                    group_id=group_id
                ).delete()

    def get_group_form_by_group_id(self, group_id: datetime):
        with self.Session() as session:
            return (
                session.query(GroupFormPreferences)
                .filter(GroupFormPreferences.group_id == group_id)
                .all()
            )
