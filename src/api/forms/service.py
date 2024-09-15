from datetime import datetime

from src.api.forms.repository import FormRepository
from src.api.exceptions import EntityNotFound
from src.api.forms.exceptions import AnswerNotFound
from src.api.forms.models import FormPreferences
from src.api.forms.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    GroupAnswerResponse,
    UserAnswerResponse,
)
from src.api.students.exceptions import StudentNotFound
from src.api.topics.exceptions import TopicNotFound
from src.api.topics.repository import TopicRepository

from src.config.logging import logger

from src.core.group_form_answer import GroupFormAnswer
from src.core.student_form_answer import StudentFormAnswer
from src.core.topic import Topic


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def add_answers(self, form_preference: FormPreferencesRequest):
        try:
            """
            Adds a new set of answers to the repository.
            """
            cleaned_user_ids = list(
                filter(
                    lambda x: x is not None,
                    [
                        form_preference.user_id_sender,
                        form_preference.user_id_student_2,
                        form_preference.user_id_student_3,
                        form_preference.user_id_student_4,
                    ]
                )
            )
            topics = [
                form_preference.topic_1,
                form_preference.topic_2,
                form_preference.topic_3,
            ]

            answers = []
            for user_id in cleaned_user_ids:
                answer = StudentFormAnswer(
                    id=user_id,
                    answer_id=form_preference.answer_id,
                    topics=topics,
                )
                answers.append(answer)

            answers_saved = self._repository.add_answers(
                answers, topics, cleaned_user_ids
            )
            return answers_saved
        except (StudentNotFound, TopicNotFound, AnswerNotFound) as e:
            message = str(e)
            logger.error(f"Entity not found: {message}")
            raise EntityNotFound(message=message)

    def delete_answers_by_answer_id(self, answer_id: datetime):
        """
        Deletes answers from the repository based on the provided answer ID.
        """
        answers = self._repository.get_answers_by_answer_id(answer_id)
        if len(answers) == 0:
            raise EntityNotFound(f"Answer id '{answer_id}' does not exists.")
        return self._repository.delete_answers_by_answer_id(answer_id)

    def _make_topic(self, topic):
        """Make a Topic based on a Topic Orm Object."""
        id = topic.id
        name = topic.name
        category = topic.category.name
        topic = Topic(id=id, title=name, category=category)
        return topic

    def _transform_topics(self, topic_repository: TopicRepository) -> dict:
        """Builds a dictionary of name: Topic with all the topics from the
        database.
        The Topic object are not ORM objects.
        """
        topics = topic_repository.get_topics()
        topcis_as_dict = dict()
        for orm_topic in topics:
            topic = self._make_topic(orm_topic)
            topcis_as_dict[topic.id] = topic

        return topcis_as_dict

    def get_answers(self, topic_repository: TopicRepository):
        """
        Retrieves answers from the repository, processes the data to group students
        by their answers, and returns a formatted response.

        Returns a list of dictionaries, each representing an answer with its associated
        students and topics, with duplicate topics removed.
        """
        db_answers = self._repository.get_answers()
        topics = self._transform_topics(topic_repository)

        response = []
        if len(db_answers) != 0:

            answers = {}
            for db_answer in db_answers:
                id = str(db_answer.answer_id.timestamp())
                topic_1 = topics[db_answer.topic_1]
                topic_2 = topics[db_answer.topic_2]
                topic_3 = topics[db_answer.topic_3]
                if id not in answers:
                    group = GroupFormAnswer(id)
                    answers[id] = group

                group = answers[id]
                group.add_student(db_answer.email)
                group.add_topics([topic_1, topic_2, topic_3])

            response = list(answers.values())

        return response

    def get_answers_by_user_id(self, user_id, topic_repository: TopicRepository):
        """
        Retrieves answers from one user based on his id
        """
        answers = self._repository.get_answers_by_user_id(user_id)
        topics = self._transform_topics(topic_repository)
        response = []
        if len(answers) != 0:

            for db_answer in answers:
                topic_1 = topics[db_answer.topic_1]
                topic_2 = topics[db_answer.topic_2]
                topic_3 = topics[db_answer.topic_3]
                response.append(
                    UserAnswerResponse(
                        answer_id=db_answer.answer_id,
                        email=db_answer.email,
                        topic_1=topic_1.name,
                        topic_2=topic_2.name,
                        topic_3=topic_3.name,
                    )
                )
        return response
