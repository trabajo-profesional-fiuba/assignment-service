from src.api.topic.schemas import TopicList
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.topic.models import Topic, Category
from src.api.tutors.repository import TutorRepository


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._topic_repository = topic_repository

    def _add_category(self, category_name: str, categories: list[Category]):
        new_category = Category(name=category_name)
        if not any(category.name == category_name for category in categories):
            categories.append(new_category)
        return categories

    def _add_topic(self, topic_name: str, category_name: str, topics: list[Topic]):
        new_topic = Topic(name=topic_name, category=category_name)
        if not any(
            (topic.name == topic_name and topic.category == category_name)
            for topic in topics
        ):
            topics.append(new_topic)
        return topics, new_topic

    def _add_topic_by_tutor(
        self, tutor: str, topics_by_tutor: dict, new_topic: Topic, capacity: int
    ):
        """
        Adds a topic and its capacity under a specific tutor in the dictionary.
        """
        if tutor not in topics_by_tutor:
            topics_by_tutor[tutor] = []
        topics_by_tutor[tutor].append({"topic": new_topic, "capacity": capacity})
        return topics_by_tutor

    def _get_info(self, rows):
        """
        Processes a list of rows containing topic names and categories, and returns
        two lists: one of unique categories and another of unique topics with their
        respective categories.
        """
        categories = []
        topics = []
        topics_by_tutor = {}
        for row in rows:
            name, category, tutor, capacity = row
            categories = self._add_category(category, categories)
            topics, new_topic = self._add_topic(name, category, topics)
            topics_by_tutor = self._add_topic_by_tutor(
                tutor, topics_by_tutor, new_topic, capacity
            )
        return categories, topics, topics_by_tutor

    def _get_content(self, csv: str):
        csv_file = TopicCsvFile(csv=csv)
        return csv_file.get_info_as_rows()

    def _get_topics_by_tutor(self, tutor_email: str, topics_by_tutor: dict):
        """
        Given a tutor's email, return a list of topic names assigned to that tutor,
        without capacities.
        """
        if tutor_email in topics_by_tutor:
            return [topic_info["topic"] for topic_info in topics_by_tutor[tutor_email]]
        else:
            return []

    def _update_tutor_periods(
        self, topics_by_tutor: dict, tutor_repository: TutorRepository
    ):
        for tutor, topics in topics_by_tutor.items():
            tutor_topics = self._get_topics_by_tutor(tutor, topics_by_tutor)
            tutor_repository.add_topics_to_period(tutor, tutor_topics)

    def _add_topics(self, topics, categories):
        self._topic_repository.add_categories(categories)
        return self._topic_repository.add_topics(topics)

    def create_topics_from_string(self, csv: str, tutor_repository: TutorRepository):
        rows = self._get_content(csv)
        categories, topics, topics_by_tutor = self._get_info(rows)
        topics = self._add_topics(topics, categories)
        self._update_tutor_periods(topics_by_tutor, tutor_repository)
        return TopicList.model_validate(topics)

    def get_topics(self):
        topics = self._topic_repository.get_topics()
        return TopicList.model_validate(topics)
