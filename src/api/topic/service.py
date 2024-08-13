from src.api.topic.schemas import TopicList, TopicResponse
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.topic.models import Topic, Category
from src.api.tutors.repository import TutorRepository

from src.config.logging import logger


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def _add_category(self, category_name: str, categories: list[Category]):
        """
        Add a category to the list if it hasn't been added yet.
        Returns a list of unique categories.
        """
        new_category = Category(name=category_name)
        if not any(category.name == category_name for category in categories):
            categories.append(new_category)
        return categories

    def _add_topic(self, topic_name: str, category_name: str, topics: list[Topic]):
        """
        Add a topic to the list if it hasn't been added yet.
        Returns a list of unique topics.
        """
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
        Processes a list of rows containing topic names, categories, tutors and
        capacities.
        Returns necessary information to create a topic:
            - Unique categories list: to add categories.
            - Unique topics list.
            - Dictionary with tutor emails as keys and a a list of dictionaries
            with topic and capacity.
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

    def _get_csv_rows(self, csv: str):
        """
        Processes a CSV string and returns its content as rows of information.
        """
        csv_file = TopicCsvFile(csv=csv)
        return csv_file.get_info_as_rows()

    def _get_topics_and_capacities_by_tutor(
        self, tutor_email: str, topics_by_tutor: dict
    ):
        """
        Given a tutor's email, return a tuple containing two lists:
            - A list of topic names assigned to that tutor.
            - A list of capacities assigned to those topics.
        """
        topics = []
        capacities = []
        for topic_info in topics_by_tutor[tutor_email]:
            topics.append(topic_info["topic"])
            capacities.append(topic_info["capacity"])
        return topics, capacities

    def _add_topic_tutor_periods(
        self, topics_by_tutor: dict, tutor_repository: TutorRepository
    ):
        """
        Add a topic tutor period entity for each topic of each tutor.
        """
        for tutor, topics_list in topics_by_tutor.items():
            tutor_topics, tutor_capacities = self._get_topics_and_capacities_by_tutor(
                tutor, topics_by_tutor
            )
            tutor_repository.add_topic_tutor_period(
                tutor, tutor_topics, tutor_capacities
            )

    def _add_topics(self, topics, categories):
        """
        Add a list of capacities and a list of topics.
        """
        self._repository.add_categories(categories)
        return self._repository.add_topics(topics)

    def create_topics_from_string(self, csv: str, tutor_repository: TutorRepository):
        """
        Processes a CSV string to create topics, categories, and tutor-topic
        assignments. Returns the list of topics added.
        """
        rows = self._get_csv_rows(csv)
        categories, topics, topics_by_tutor = self._get_info(rows)
        topics = self._add_topics(topics, categories)
        self._add_topic_tutor_periods(topics_by_tutor, tutor_repository)
        return TopicList.model_validate(topics)

    def get_topics(self):
        topics = self._repository.get_topics()
        return TopicList.model_validate(topics)

    def get_or_add_topic(self, topic_name: str):
        """
        Attempts to retrieve the topic from the database.
        if the topic is not in db, it creates it with a
        default category
        """
        topic_db = self._repository.get_topic_by_name(topic_name)
        if not topic_db:
            logger.info(
                f"Topic name {topic_name} is not in db, adding it with default category"
            )
            topic_db = self._repository.add_topic(
                Topic(name=topic_name, category="default")
            )
        return TopicResponse.model_validate(topic_db)
