from sqlalchemy.orm import Session
from datetime import datetime

from src.api.form.models import FormPreferences
from src.api.exceptions import Duplicated

from src.api.student.exceptions import StudentNotFound
from src.api.topic.exceptions import TopicNotFound
from src.api.users.model import User, Role
from src.api.topic.models import Topic

from src.config.logging import logger


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _verify_topics(self, session, topics: list[str]):
        ids = []
        for topic in topics:
            found = session.query(Topic).filter_by(name=topic).first()
            if found:
                ids.append(found.id)
            else:
                logger.error(f"Topic '{topic}' not found in db")
                raise TopicNotFound(f"Topic '{topic}' not found.")
        return ids

    def _verify_user(self, session, user_id: int):
        user = session.query(User).filter_by(id=user_id).first()
        if not user or user.role != Role.STUDENT:
            logger.error(f"User with id: {user_id} is not in db")
            raise StudentNotFound(
                message=f"Be sure that the id: {user_id} is a valid student."
            )

    def _verify_answer(self, session, topics_id: list[int], user_ids: list[int]):
        count = 0
        topic_1_id, topic_2_id, topic_3_id = topics_id
        for user_id in user_ids:
            answer = (
                session.query(FormPreferences)
                .filter_by(
                    user_id=user_id,
                    topic_1=topic_1_id,
                    topic_2=topic_2_id,
                    topic_3=topic_3_id,
                )
                .first()
            )
            if answer is not None:
                count += 1
        if count == len(user_ids):
            logger.error(f"Answer duplicated send by ")
            raise Duplicated(message="The answer already exists.")

    def add_answers(
        self, answers: list[FormPreferences], topics: list[str], user_ids: list[int]
    ):
        with self.Session() as session:
            topic_ids = self._verify_topics(session, topics)
            self._verify_answer(session, topic_ids, user_ids)
            for answer in answers:
                self._verify_user(session, answer.user_id)
                answer = FormPreferences(
                    user_id=answer.user_id,
                    answer_id=answer.answer_id,
                    topic_1=topic_ids[0],
                    topic_2=topic_ids[1],
                    topic_3=topic_ids[2],
                )
                session.add(answer)
            session.commit()
            logger.info(f"New {len(answers)} introduced")
            session.expunge_all()

        return answers

    def delete_answers_by_answer_id(self, answer_id: datetime):
        with self.Session() as session:
            with session.begin():
                session.query(FormPreferences).filter_by(answer_id=answer_id).delete()

    def get_answers_by_answer_id(self, answer_id: datetime):
        with self.Session() as session:
            answers = (
                session.query(FormPreferences)
                .filter(FormPreferences.answer_id == answer_id)
                .all()
            )
            session.expunge_all()
            logger.info(f"Look for answers of {answer_id}")

        return answers

    def get_answers(self):
        with self.Session() as session:
            answers = (
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
            session.expunge_all()
            logger.info(f"Get all the answers")

        return answers
