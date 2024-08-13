from src.api.groups.exceptions import GroupError
from src.api.groups.schemas import GroupResponse


class GroupService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_assigned_group(self, ids, period_id, topic_id):
        group = self._repository.add_group(ids, period_id, topic_id)
        return GroupResponse.model_validate(group)

    def create_basic_group(self, ids, preferred_topics=[]):
        try:
            group = self._repository.add_group(
                ids=ids, preferred_topics=preferred_topics
            )
            return GroupResponse.model_validate(group)
        except Exception:
            raise GroupError(message="Group could't be created")
