from datetime import datetime
from collections import defaultdict

from src.api.forms.repository import FormRepository
from src.api.forms.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    UserAnswerList,
    GroupAnswerResponse,
    UserAnswerResponse,
)
from src.api.forms.exceptions import (
    AnswerNotFound,
)
from src.api.exceptions import EntityNotFound
from src.api.forms.models import FormPreferences
from src.api.topics.repository import TopicRepository

from src.api.students.exceptions import StudentNotFound
from src.api.topics.exceptions import TopicNotFound
from src.config.logging import logger
from src.core.group_answer import GroupFormAnswer
from src.core.topic import Topic


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def _filter_user_ids(self, user_ids: list[int]):
        """
        Filters out 'None' values from a list of university IDs.

        Returns a list of university IDs with 'None' values removed.
        """
        filtered_user_ids = []
        for user_id in user_ids:
            if user_id is not None:
                filtered_user_ids.append(user_id)
        return filtered_user_ids

    def add_answers(self, form_preference: FormPreferencesRequest):
        try:
            """
            Adds a new set of answers to the repository.
            """
            cleaned_user_ids = self._filter_user_ids(
                [
                    form_preference.user_id_sender,
                    form_preference.user_id_student_2,
                    form_preference.user_id_student_3,
                    form_preference.user_id_student_4,
                ]
            )
            topics = [
                form_preference.topic_1,
                form_preference.topic_2,
                form_preference.topic_3,
            ]

            answers = []
            for user_id in cleaned_user_ids:
                answer = FormPreferences(
                    user_id=user_id,
                    answer_id=form_preference.answer_id,
                    topic_1=form_preference.topic_1,
                    topic_2=form_preference.topic_2,
                    topic_3=form_preference.topic_3,
                )
                answers.append(answer)

            answers_saved = self._repository.add_answers(
                answers, topics, cleaned_user_ids
            )
            return FormPreferencesList.model_validate(answers_saved)
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
        id = topic.id
        name = topic.name
        category = topic.category.name
        topic = Topic(id=id,title=name,category=category)
        return topic

    def get_answers(self, topic_repository: TopicRepository):
        """
        Retrieves answers from the repository, processes the data to group students
        by their answers, and returns a formatted response.

        Returns a list of dictionaries, each representing an answer with its associated
        students and topics, with duplicate topics removed.
        """
        db_answers = self._repository.get_answers()
        response = []
        if len(db_answers) != 0:

            answers = {}
            for db_answer in db_answers:
                id = str(db_answer.answer_id.timestamp())
                topic_1 = self._make_topic(topic_repository.get_topic_by_id(db_answer.topic_1))
                topic_2 = self._make_topic(topic_repository.get_topic_by_id(db_answer.topic_2))
                topic_3 = self._make_topic(topic_repository.get_topic_by_id(db_answer.topic_3))
                if id not in answers:
                    group = GroupFormAnswer(id)
                    answers[id] = group

                group = answers[id] 
                group.add_student(db_answer.email)
                group.add_topics([topic_1, topic_2, topic_3])

            
            for answer_id, data in answers.items():
                response.append(
                    GroupAnswerResponse(
                        id=answer_id,
                        students=data.students,
                        topics=data.get_topic_names(),
                    )
                )

        return response 
