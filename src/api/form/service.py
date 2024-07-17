from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupFormRequest


class FormService:

    def __init__(self, form_repository: FormRepository):
        self._repository = form_repository

    def add_group_submition(self, group_form: GroupFormRequest):

        resp = self._repository.add_group_form(group_form)
