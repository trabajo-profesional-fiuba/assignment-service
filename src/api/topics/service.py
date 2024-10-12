from src.api.exceptions import EntityNotFound

from src.api.topics.models import Topic, Category
from src.api.topics.repository import TopicRepository
from src.api.topics.schemas import TopicList, TopicRequest, TopicResponse
from src.api.topics.utils import TopicCsvFile

from src.api.tutors.exceptions import TutorNotFound, TutorPeriodNotFound
from src.api.tutors.repository import TutorRepository

from src.config.logging import logger


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def _get_categories_mapped(self):
        # looks for all the categories and create a diccionary to map name:id
        categories = self._repository.get_categories()
        id_by_categories = {}
        for category in categories:
            id_by_categories[category.name] = category.id

        return id_by_categories

    #
    def _get_topics_and_capacities_by_tutor(
        self, tutor_email: str, topics_by_tutor: dict
    ):
        """
        Given a tutor's email, return a tuple containing two lists:
            - A list of topic names assigned to that tutor.
            - A list of capacities assigned to those topics.
        """
        id_by_categories = self._get_categories_mapped()
        topics = []
        capacities = []
        for topic_info in topics_by_tutor[tutor_email]:
            name = topic_info["topic"]
            category = id_by_categories[topic_info["category"]]
            topic = Topic(name=name, category_id=category)
            topics.append(topic)
            capacities.append(topic_info["capacity"])
        return topics, capacities

    def _add_topic_tutor_periods(
        self, period_id: str, topics_by_tutor: dict, tutor_repository: TutorRepository
    ):
        """
        Add a topic tutor period entity for each topic of each tutor.
        """
        for tutor, _ in topics_by_tutor.items():
            tutor_topics, tutor_capacities = self._get_topics_and_capacities_by_tutor(
                tutor, topics_by_tutor
            )
            tutor_repository.add_topic_tutor_period(
                period_id, tutor, tutor_topics, tutor_capacities
            )

    def _add_categories(self, categories):
        """
        Add a list of categories.
        """
        categories_db = []
        for category in categories:
            category_db = Category(name=category)
            categories_db.append(category_db)
        categories_saved = self._repository.add_categories(categories_db)
        logger.info("Categories already created.")

        return categories_saved

    def _add_topics(self, topics: list[tuple[str, str]]):
        """
        Add a list of list of topics.
        """

        id_by_categories = self._get_categories_mapped()

        # Make Topic ORM objs based on the name and category
        topics_db = []
        for topic in topics:
            category_id = id_by_categories[topic[1]]
            topic_db = Topic(name=topic[0], category_id=category_id)
            topics_db.append(topic_db)
        topics = self._repository.add_topics(topics_db)
        logger.info("Topics already created.")

        return topics

    def create_topics_from_string(
        self, period_id: str, csv: str, tutor_repository: TutorRepository
    ):
        """
        Processes a CSV string to create topics, categories, and tutor-topic
        assignments. Deletes existing topics if applies and returns the list
        of topics created.
        """
        try:
            csv_file = TopicCsvFile(csv=csv)
            categories = csv_file.get_categories()
            topics = csv_file.get_topics()
            topics_by_tutor = csv_file.get_topics_by_tutor()

            self._repository.delete_topics()

            self._add_categories(categories)
            db_topics = self._add_topics(topics)

            self._add_topic_tutor_periods(period_id, topics_by_tutor, tutor_repository)

            return TopicList.model_validate(db_topics)
        except (TutorNotFound, TutorPeriodNotFound) as e:
            raise EntityNotFound(str(e))

    def get_topics(self):
        db_topics = self._repository.get_topics()
        return TopicList.model_validate(db_topics)

    def get_or_add_topic(self, topic_name: str):
        """
        Attempts to retrieve the topic from the database.
        if the topic is not in db, it creates it with a
        default category
        """
        db_topic = self._repository.get_topic_by_name(topic_name)
        if not db_topic:
            logger.info(
                f"Topic name {topic_name} is not in db, adding it with default category"
            )
            db_topic = self._repository.add_topic(Topic(name=topic_name, category_id=1))
        return TopicResponse.model_validate(db_topic)

    def get_topics_by_period(self, period_id):
        db_topics = self._repository.get_topics_by_period_id(period_id)
        return db_topics

    def add_category(self, categoy_name: str):
        category = self._repository.add_category(Category(name=categoy_name))
        return category

    def add_topic(self, topic_req: TopicRequest):
        topic = self._repository.add_topic_with_category(
            Topic(name=topic_req.name), topic_req.category
        )
        return topic
