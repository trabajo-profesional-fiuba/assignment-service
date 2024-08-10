from src.api.topic.schemas import TopicList
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.topic.models import Topic, Category
from src.api.tutors.repository import TutorRepository


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._topic_repository = topic_repository

    def add_category(self, category_name: str, categories: list[Category]):
        new_category = Category(name=category_name)
        if not any(category.name == category_name for category in categories):
            categories.append(new_category)
        return categories

    def add_topic(self, topic_name: str, category_name: str, topics: list[Topic]):
        new_topic = Topic(name=topic_name, category=category_name)
        if not any(
            (topic.name == topic_name and topic.category == category_name)
            for topic in topics
        ):
            topics.append(new_topic)
        return topics, new_topic

    def add_topic_by_tutor(self, tutor: str, topics_by_tutor: dict, new_topic: Topic):
        if tutor not in topics_by_tutor:
            topics_by_tutor[tutor] = []
        topics_by_tutor[tutor].append(new_topic)
        return topics_by_tutor

    def get_categories_topics_tutors(self, rows):
        """
        Processes a list of rows containing topic names and categories, and returns
        two lists: one of unique categories and another of unique topics with their
        respective categories.
        """
        categories = []
        topics = []
        topics_by_tutor = {}
        for row in rows:
            name, category, tutor = row
            categories = self.add_category(category, categories)
            topics, new_topic = self.add_topic(name, category, topics)
            topics_by_tutor = self.add_topic_by_tutor(tutor, topics_by_tutor, new_topic)
        return categories, topics, topics_by_tutor

    def create_topics_from_string(self, csv: str, tutor_repository: TutorRepository):
        csv_file = TopicCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        categories, topics, topics_by_tutor = self.get_categories_topics_tutors(rows)
        self._topic_repository.add_categories(categories)
        result = self._topic_repository.add_topics(topics)
        for tutor, topics in topics_by_tutor.items():
            tutor_repository.add_topics_to_period(tutor, topics)
        return TopicList.model_validate(result)

    def get_topics(self):
        topics = self._topic_repository.get_topics()
        return TopicList.model_validate(topics)
