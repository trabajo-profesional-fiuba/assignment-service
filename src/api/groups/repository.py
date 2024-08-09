from sqlalchemy.orm import Session
from src.api.groups.models import Group
from src.api.users.model import User, Role


class GroupRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group(self, ids, period_id = None, topic_id = None):
        with self.Session() as session:
            group = Group(tutor_period_id=period_id, assigned_topic_id=topic_id)
            students = session.query(User).filter(User.id.in_(ids)).all()
            group.students = students
            session.add(group)
            session.commit()
            session.refresh(group)
            session.expunge(group)
        
        return group