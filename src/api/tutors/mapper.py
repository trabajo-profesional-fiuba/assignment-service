from src.core.topic import Topic
from src.core.tutor import SinglePeriodTutor


class TutorMapper:

    def convert_from_periods_to_single_period_tutors(self, db_periods):
        tutors = list()
        for db_period in db_periods:
            db_tutor = db_period.tutor
            topics = [
                Topic(
                    id=topic.id,
                    title=topic.name,
                    category=topic.category.name,
                    capacity=1,
                )
                for topic in db_period.topics
            ]
            tutor = SinglePeriodTutor(
                id=db_tutor.id,
                period_id=db_period.id,
                name=db_tutor.name,
                last_name=db_tutor.last_name,
                email=db_tutor.email,
                topics=topics,
                capacity=db_period.capacity,
            )
            tutors.append(tutor)

        return tutors
