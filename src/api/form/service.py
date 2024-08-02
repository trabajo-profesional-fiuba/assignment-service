from datetime import datetime

from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormRequest
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

    def add_answers(self, group_form: GroupFormRequest):
        cleaned_uids = self._filter_uids(
            [
                group_form.uid_sender,
                group_form.uid_student_2,
                group_form.uid_student_3,
                group_form.uid_student_4,
            ]
        )
        return self._repository.add_answers(group_form, cleaned_uids)

    def delete_answers_by_answer_id(self, answer_id: datetime):
        group_forms = self._repository.get_answers_by_answer_id(answer_id)
        if len(group_forms) == 0:
            raise AnswerIdNotFound(f"Group id '{answer_id}' does not exists.")
        return self._repository.delete_answers_by_answer_id(answer_id)

    def get_answers(self):
        return self._repository.get_answers()
