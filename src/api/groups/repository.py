from sqlalchemy.orm import Session
from src.api.students.exceptions import StudentNotFound
from src.api.groups.models import Group
from src.api.users.models import User


class GroupRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group(self, ids, period_id=None, topic_id=None, preferred_topics=[]):
        with self.Session() as session:
            group = Group(
                tutor_period_id=period_id,
                assigned_topic_id=topic_id,
                preferred_topics=preferred_topics,
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
