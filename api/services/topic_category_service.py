from api.models import TopicCategoryItem
from api.repositories.topic_category_repository import TopicCategoryRepository
from api.exceptions import TopicCategoryDuplicated


class TopicCategoryService:

    def __init__(self, repository: TopicCategoryRepository):
        self._repository = repository

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            if self._repository.get_topic_category_by_name(topic_category.name) is None:
                return self._repository.add_topic_category(topic_category)
            raise TopicCategoryDuplicated(
                f"Topic category '{topic_category.name}' already exists."
            )
        except Exception as err:
            raise err
