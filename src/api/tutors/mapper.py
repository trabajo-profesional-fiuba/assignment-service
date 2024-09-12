from src.core.topic import Topic
from src.core.tutor import SinglePeriodTutor


class TutorMapper:

    def convert_from_periods_to_single_period_tutors(self, db_tutors):
        tutors = list()
        for db_periods in db_tutors:
            db_tutor = db_periods.tutor
            topics = [
                Topic(
                    id=topic.id,
                    title=topic.name,
                    category=topic.category.name,
                    capacity=1,
                )
                for topic in db_periods.topics
            ]
            tutor = SinglePeriodTutor(
                id=db_tutor.id,
                name=db_tutor.name,
                last_name=db_tutor.last_name,
                email=db_tutor.email,
                topics=topics,
                capacity=db_periods.capacity,
            )
            tutors.append(tutor)

        return tutors
