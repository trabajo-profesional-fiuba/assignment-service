from src.api.auth.jwt import JwtResolver
from src.api.forms.models import FormPreferences
from src.api.forms.repository import FormRepository
from src.api.groups.repository import GroupRepository
from src.api.topics.models import Category, Topic
from src.api.topics.repository import TopicRepository
from src.config.database.database import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.tutors.models import Period, TutorPeriod

from src.api.users.repository import UserRepository
from src.api.users.models import User, Role

from src.api.auth.hasher import ShaHasher
import datetime as dt


class ApiHelper:
    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)
    hasher = ShaHasher()

    def __init__(self):
        self._user_repository = UserRepository(self.Session)
        self._tutor_repository = TutorRepository(self.Session)
        self._topic_repository = TopicRepository(self.Session)
        self._groups_repository = GroupRepository(self.Session)
        self._form_repository = FormRepository(self.Session)

    def create_period(self, period: str):
        self._tutor_repository.add_period(Period(id=period))

    def create_tutor(self, name: str, last_name: str, id: str, email: str):
        tutor = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.TUTOR,
        )

        self._user_repository.add_tutors([tutor])

    def create_student(self, name: str, last_name: str, id: str, email: str):
        student = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.STUDENT,
        )

        self._user_repository.add_students([student])

    def create_tutor_period(self, tutor_id: int, period_id: str, capacity: int = 1):
        period = TutorPeriod(tutor_id=tutor_id, period_id=period_id, capacity=capacity)
        self._tutor_repository.add_tutor_periods([period])

    def get_tutor_by_tutor_id(self, tutor_id):
        return self._tutor_repository.get_tutor_by_tutor_id(tutor_id)

    def create_admin_token(self):
        sub = {
            "id": 1,
            "name": "admin",
            "last_name": "admin",
            "role": "admin",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "admin")
        return token

    def create_student_token(self):
        sub = {
            "id": 1,
            "name": "student",
            "last_name": "student",
            "role": "student",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "student")
        return token

    def create_topic(self, name: str, category_id: int):
        topic = Topic(name=name, category_id=category_id)
        self._topic_repository.add_topic(topic)

    def create_category(self, name: str):
        category = Category(name=name)
        self._topic_repository.add_category(category)

    def create_default_topics(self, topic_names):
        for name in topic_names:
            topic = Topic(name=name, category_id=1)
            self._topic_repository.add_topic(topic)

    def add_tutor_to_topic(self, period_id, tutor_email, topics, capacities):
        topics_db = [Topic(name=t, category_id=1) for t in topics]

        self._tutor_repository.add_topic_tutor_period(
            period_id, tutor_email, topics_db, capacities
        )

    def get_groups(self, period_id=None):
        return self._groups_repository.get_groups(period=period_id)

    def register_answer(self, ids, topics):
        today = dt.datetime.today().isoformat()
        all_topics = self._topic_repository.get_topics()
        all_topics_dict = dict()
        for topic in all_topics:
            all_topics_dict[topic.name] = topic.id

        answers = []
        for id in ids:
            answer = FormPreferences(
                user_id=id,
                answer_id=today,
                topic_1=all_topics_dict[topics[0]],
                topic_2=all_topics_dict[topics[1]],
                topic_3=all_topics_dict[topics[2]],
            )
            answers.append(answer)
        self._form_repository.add_answers(answers, topics, ids)

    def create_basic_group(self, ids, topics):
        self._groups_repository.add_group(ids=ids, preferred_topics=topics)
