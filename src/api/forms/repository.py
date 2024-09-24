from datetime import datetime
from sqlalchemy.orm import Session

from src.api.exceptions import Duplicated
from src.api.forms.models import FormPreferences
from src.api.students.exceptions import StudentNotFound
from src.api.topics.exceptions import TopicNotFound
from src.api.topics.models import Topic
from src.api.users.models import User, Role

from src.config.logging import logger
from src.core.student_form_answer import StudentFormAnswer


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _verify_topics(self, session, topic_names: list[str]):

        topics = session.query(Topic).filter(Topic.name.in_(topic_names)).all()
        topic_id_map = {topic.name: topic.id for topic in topics}

        missing_topics = set(topic_names) - set(topic_id_map.keys())
        if missing_topics:
            raise TopicNotFound(f"Topics not found: {', '.join(missing_topics)}")

        ids = [topic_id_map[topic] for topic in topic_names]

        return ids

    def _verify_users_exists(self, session, user_ids: list[int]):
        users = session.query(User).filter(User.id.in_(user_ids)).all()

        if len(users) != len(user_ids):
            raise StudentNotFound(message="Be sure that all the ids are students")

        for user in users:
            if not user or user.id not in user_ids or user.role != Role.STUDENT:
                logger.error(f"User with id: {user.id} is not in db")
                raise StudentNotFound(
                    message=f"Be sure that the id: {user.id} is a valid student."
                )

    def _verify_answer(self, session, topics_id: list[int], user_ids: list[int]):
        topic_1_id, topic_2_id, topic_3_id = topics_id
        answers = (
            session.query(FormPreferences)
            .filter(
                FormPreferences.user_id.in_(user_ids),
                FormPreferences.topic_1 == topic_1_id,
                FormPreferences.topic_2 == topic_2_id,
                FormPreferences.topic_3 == topic_3_id,
            )
            .all()
        )
        if len(answers) == len(user_ids):
            logger.error("Answer duplicated")
            raise Duplicated(message="The answer already exists.")

    def add_answers(
        self, answers: list[StudentFormAnswer], topics: list[str], user_ids: list[int]
    ):
        with self.Session() as session:
            topic_ids = self._verify_topics(session, topics)
            self._verify_users_exists(session, user_ids)
            self._verify_answer(session, topic_ids, user_ids)
            for answer in answers:
                answer = FormPreferences(
                    user_id=answer.id,
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

    def get_answers_by_user_id(self, user_id):
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
                .filter(FormPreferences.user_id == user_id)
                .all()
            )
            session.expunge_all()
            logger.info("Get all the answers")

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
            logger.info("Get all the answers")

        return answers
