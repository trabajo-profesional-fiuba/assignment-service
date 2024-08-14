from datetime import datetime
from collections import defaultdict

from src.api.form.repository import FormRepository
from src.api.form.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    UserAnswerList,
    GroupAnswerResponse,
)
from src.api.form.exceptions import (
    StudentNotFound,
    TopicNotFound,
    AnswerNotFound,
)
from src.api.exceptions import EntityNotFound
from src.api.form.models import FormPreferences

from src.config.logging import logger


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

    def _get_students_topics(self, answers: UserAnswerList):
        """
        Extracts students and their associated topics from database items.
        """
        result = defaultdict(lambda: {"students": [], "topics": []})
        for answer in answers:
            answer_id = answer.answer_id
            result[answer_id]["students"].append(answer.email)
            result[answer_id]["topics"].extend(
                [answer.topic_1, answer.topic_2, answer.topic_3]
            )
        return result

    def get_answers(self):
        """
        Retrieves answers from the repository, processes the data to group students
        by their answers, and returns a formatted response.

        Returns a list of dictionaries, each representing an answer with its associated
        students and topics, with duplicate topics removed.
        """
        answers = UserAnswerList.model_validate(self._repository.get_answers())
        students_topics = self._get_students_topics(answers)
        return [
            GroupAnswerResponse(
                answer_id=answer_id,
                students=data["students"],
                topics=list(set(data["topics"])),
            )
            for answer_id, data in students_topics.items()
        ]
