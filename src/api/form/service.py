from datetime import datetime
from collections import defaultdict

from src.api.form.repository import FormRepository
from src.api.form.schemas import (
    FormPreferencesRequest,
    UserAnswerResponse,
    GroupAnswerResponse,
)
from src.api.form.exceptions import AnswerIdNotFound


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

    def add_answers(self, answers: FormPreferencesRequest):
        """
        Adds a new set of answers to the repository.
        """
        cleaned_user_ids = self._filter_user_ids(
            [
                answers.user_id_sender,
                answers.user_id_student_2,
                answers.user_id_student_3,
                answers.user_id_student_4,
            ]
        )
        return self._repository.add_answers(answers, cleaned_user_ids)

    def delete_answers_by_answer_id(self, answer_id: datetime):
        """
        Deletes answers from the repository based on the provided answer ID.
        """
        answers = self._repository.get_answers_by_answer_id(answer_id)
        if len(answers) == 0:
            raise AnswerIdNotFound(f"Group id '{answer_id}' does not exists.")
        return self._repository.delete_answers_by_answer_id(answer_id)

    def _get_students_topics(self, answers: list[UserAnswerResponse]):
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
        db_items = self._repository.get_answers()
        students_topics = self._get_students_topics(db_items)
        return [
            GroupAnswerResponse(
                answer_id=answer_id,
                students=data["students"],
                topics=list(set(data["topics"])),
            )
            for answer_id, data in students_topics.items()
        ]
