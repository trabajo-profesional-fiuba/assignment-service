from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormRequest


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def filter_uids(self, uids: list[int]):
        """
        Returns not none university ids.
        """
        filtered_uids = []
        for uid in uids:
            if uid is not None:
                filtered_uids.append(uid)
        return filtered_uids

    def add_group_preferences(self, group_form: GroupFormRequest):
        try:
            cleaned_uids = self.filter_uids(
                [
                    group_form.uid_sender,
                    group_form.uid_student_2,
                    group_form.uid_student_3,
                    group_form.uid_student_4,
                ]
            )
            return self._repository.add_group_form(group_form, cleaned_uids)
        except Exception as err:
            raise err
