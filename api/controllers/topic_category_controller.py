from api.models import TopicCategoryItem


class TopicCategoryController:

    def __init__(self):
        pass

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            return topic_category
        except Exception as err:
            raise err