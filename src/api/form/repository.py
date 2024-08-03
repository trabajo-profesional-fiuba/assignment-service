from sqlalchemy import exc
from sqlalchemy.orm import Session
from datetime import datetime

from src.api.form.schemas import (
    FormPreferencesRequest,
    FormPreferencesResponse,
    UserAnswerResponse,
)
from src.api.form.models import FormPreferences
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

    def _verify_user(self, session, user_id: int):
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise StudentNotFound(f"Student with user_id '{user_id}' not found.")
        if user.rol != Role.STUDENT:
            raise StudentNotFound("The student must have the role 'student'.")

    def _verify_answer(
        self, session, answers: FormPreferencesRequest, user_ids: list[int]
    ):
        count = 0
        for user_id in user_ids:
            answer = (
                session.query(FormPreferences)
                .filter_by(
                    user_id=user_id,
                    topic_1=answers.topic_1,
                    topic_2=answers.topic_2,
                    topic_3=answers.topic_3,
                )
                .first()
            )
            if answer is not None:
                count += 1
        if count == len(user_ids):
            raise DuplicatedAnswer("The answer already exists.")

    def add_answers(self, answers: FormPreferencesRequest, user_ids: list[int]):
        with self.Session() as session:
            with session.begin():
                db_items = []
                response = []
                self._verify_topics(
                    session,
                    [answers.topic_1, answers.topic_2, answers.topic_3],
                )
                self._verify_answer(session, answers, user_ids)
                for user_id in user_ids:
                    self._verify_user(session, user_id)
                    db_item = FormPreferences(
                        user_id=user_id,
                        answer_id=answers.answer_id,
                        topic_1=answers.topic_1,
                        topic_2=answers.topic_2,
                        topic_3=answers.topic_3,
                    )
                    db_items.append(db_item)
                    response.append(FormPreferencesResponse.model_validate(db_item))
                session.add_all(db_items)
                return response

    def delete_answers_by_answer_id(self, answer_id: datetime):
        with self.Session() as session:
            with session.begin():
                session.query(FormPreferences).filter_by(answer_id=answer_id).delete()

    def get_answers_by_answer_id(self, answer_id: datetime):
        with self.Session() as session:
            return (
                session.query(FormPreferences)
                .filter(FormPreferences.answer_id == answer_id)
                .all()
            )

    def get_answers(self):
        with self.Session() as session:
            response = []
            db_items = (
                session.query(
                    FormPreferences.answer_id,
                    User.email.label("email"),
                    FormPreferences.topic_1,
                    FormPreferences.topic_2,
                    FormPreferences.topic_3,
                )
                .join(User, User.id == FormPreferences.user_id)
                .all()
            )
            for db_item in db_items:
                response.append(UserAnswerResponse.model_validate(db_item))
            return response
