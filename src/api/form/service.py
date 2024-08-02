from datetime import datetime
from collections import defaultdict

from src.api.form.repository import FormRepository
from src.api.form.schemas import FormPreferencesRequest
from src.api.form.exceptions import AnswerIdNotFound


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def _filter_uids(self, uids: list[int]):
        """
        Returns not none university ids.
        """
        filtered_uids = []
        for uid in uids:
            if uid is not None:
                filtered_uids.append(uid)
        return filtered_uids

    def add_answers(self, answers: FormPreferencesRequest):
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
        answerss = self._repository.get_answers_by_answer_id(answer_id)
        if len(answerss) == 0:
            raise AnswerIdNotFound(f"Group id '{answer_id}' does not exists.")
        return self._repository.delete_answers_by_answer_id(answer_id)

    def get_answers(self):
        answers = self._repository.get_answers()

        result = defaultdict(lambda: {"students": [], "topics": []})
        for answer in answers:
            answer_id = answer.answer_id
            result[answer_id]["students"].append(answer.email)
            result[answer_id]["topics"].extend(
                [answer.topic_1, answer.topic_2, answer.topic_3]
            )

        response_data = [
            {
                "answer_id": answer_id,
                "students": data["students"],
                "topics": list(set(data["topics"])),
            }
            for answer_id, data in result.items()
        ]
        return response_data
