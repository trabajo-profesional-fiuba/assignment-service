from datetime import datetime
from collections import defaultdict

from src.api.form.repository import FormRepository
from src.api.form.schemas import FormPreferencesRequest, UserAnswerResponse
from src.api.form.exceptions import AnswerIdNotFound


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def _filter_uids(self, uids: list[int]):
        """
        Filters out 'None' values from a list of university IDs.

        Returns a list of university IDs with 'None' values removed.
        """
        filtered_uids = []
        for uid in uids:
            if uid is not None:
                filtered_uids.append(uid)
        return filtered_uids

    def add_answers(self, answers: FormPreferencesRequest):
        """
        Adds a new set of answers to the repository.
        """
        cleaned_uids = self._filter_uids(
            [
                answers.uid_sender,
                answers.uid_student_2,
                answers.uid_student_3,
                answers.uid_student_4,
            ]
        )
        return self._repository.add_answers(answers, cleaned_uids)

    def delete_answers_by_answer_id(self, answer_id: datetime):
        """
        Deletes answers from the repository based on the provided answer ID.
        """
        answers = self._repository.get_answers_by_answer_id(answer_id)
        if len(answers) == 0:
            raise AnswerIdNotFound(f"Group id '{answer_id}' does not exists.")
        return self._repository.delete_answers_by_answer_id(answer_id)

    def _get_students_topics(self, db_items: list[UserAnswerResponse]):
        """
        Extracts students and their associated topics from database items.
        """
        result = defaultdict(lambda: {"students": [], "topics": []})
        for db_item in db_items:
            answer_id = db_item.answer_id
            result[answer_id]["students"].append(db_item.email)
            result[answer_id]["topics"].extend(
                [db_item.topic_1, db_item.topic_2, db_item.topic_3]
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
        response = [
            {
                "answer_id": answer_id,
                "students": data["students"],
                "topics": list(set(data["topics"])),
            }
            for answer_id, data in students_topics.items()
        ]
        return response
