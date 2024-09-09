from sqlalchemy.orm import Session
from src.api.groups.models import Group
from src.api.students.exceptions import StudentNotFound
from src.api.tutors.models import TutorPeriod
from src.api.users.models import User


class GroupRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group(self, ids, tutor_period_id=None, topic_id=None, preferred_topics=[], period_id=None):
        with self.Session() as session:
            group = Group(
                tutor_period_id=tutor_period_id,
                assigned_topic_id=topic_id,
                preferred_topics=preferred_topics,
                period_id=period_id
            )
            students = session.query(User).filter(User.id.in_(ids)).all()
            group.students = students
            if len(students) != len(ids):
                raise StudentNotFound(message="Some ids are not in database")
            session.add(group)
            session.commit()
            session.refresh(group)
            session.expunge(group)

        return group

    def get_groups(self, period):
        """Returns all groups for a specific period"""
        with self.Session() as session:
            groups = (
                session.query(Group)
                .filter(Group.period_id == period)
                .all()
            )
            session.expunge_all()
        
        return groups
