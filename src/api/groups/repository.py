from sqlalchemy import func, bindparam, update
from sqlalchemy.orm import Session, joinedload

from src.api.groups.exceptions import GroupNotFound
from src.api.groups.models import Group, association_table
from src.api.students.exceptions import StudentNotFound
from src.api.users.models import User


class GroupRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group(
        self,
        ids,
        tutor_period_id=None,
        topic_id=None,
        preferred_topics=[],
        period_id=None,
    ):
        with self.Session() as session:
            group = Group(
                tutor_period_id=tutor_period_id,
                assigned_topic_id=topic_id,
                preferred_topics=preferred_topics,
                period_id=period_id,
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

    def add_group_having_emails(
        self,
        emails,
        tutor_period_id=None,
        topic_id=None,
        preferred_topics=[],
        period_id=None,
    ):
        with self.Session() as session:
            group = Group(
                tutor_period_id=tutor_period_id,
                assigned_topic_id=topic_id,
                preferred_topics=preferred_topics,
                period_id=period_id,
            )
            students = session.query(User).filter(User.email.in_(emails)).all()
            group.students = students
            if len(students) != len(emails):
                raise StudentNotFound(message="Some ids are not in database")
            session.add(group)
            session.commit()
            session.refresh(group)
            session.expunge(group)

        return group

    def get_groups(self, period) -> list[Group]:
        """Returns all groups for a given period"""
        with self.Session() as session:
            groups = (
                session.query(Group)
                .options(
                    joinedload(Group.topic),
                    joinedload(Group.tutor_period),
                    joinedload(Group.period),
                    joinedload(Group.students),
                )
                .filter(Group.period_id == period)
                .all()
            )
            session.expunge_all()
        return groups

    def get_groups_without_tutor_and_period(self) -> list[Group]:
        with self.Session() as session:
            groups = (
                session.query(Group)
                .filter(Group.assigned_topic_id.is_(None))
                .filter(Group.tutor_period_id.is_(None))
                .all()
            )
            session.expunge_all()

        return groups

    def get_groups_without_preferred_topics(self) -> list[Group]:
        with self.Session() as session:
            groups = (
                session.query(Group)
                .filter(func.cardinality(Group.preferred_topics) == 0)
                .all()
            )
            session.expunge_all()

        return groups

    def get_groups_learning_path(self, period) -> list[Group]:
        """Returns all groups learning path information for a given period"""
        with self.Session() as session:
            groups = session.query(Group).filter(Group.period_id == period).all()
        return groups

    def bulk_update(self, groups_to_update: list[dict], period: str):
        stmt = (
            update(Group)
            .where(Group.id == bindparam("b_id"))
            .values(
                assigned_topic_id=bindparam("b_assigned_topic_id"),
                tutor_period_id=bindparam("b_tutor_period_id"),
            )
        )
        with self.Session() as session:
            session.connection().execute(
                stmt,
                groups_to_update,
            )
            session.commit()

    def update(self, group_id, attributes: dict):
        stmt = update(Group).where(Group.id == group_id).values(**attributes)
        with self.Session() as session:
            session.execute(stmt)
            session.commit()

    def get_groups_by_period_id(self, tutor_period_id) -> list[Group]:
        """Returns all groups for a given assigned_tutor_period"""
        with self.Session() as session:
            groups = (
                session.query(Group)
                .options(
                    joinedload(Group.topic),
                    joinedload(Group.tutor_period),
                    joinedload(Group.period),
                    joinedload(Group.students),
                )
                .filter(Group.tutor_period_id == tutor_period_id)
                .all()
            )
            session.expunge_all()
        return groups

    def get_group_by_id(self, group_id) -> Group:
        with self.Session() as session:
            group = session.query(Group).filter(Group.id == group_id).one_or_none()
            if group is None:
                raise GroupNotFound(message=f"{group_id} not found in db")

            session.expunge(group)
        return group

    def get_group_by_student_id(self, student_id: int) -> Group:
        with self.Session() as session:
            result = (
                session.query(association_table.c.group_id.label('id'))
                .filter_by(student_id=student_id)
                .one_or_none()
            )
            if result is None:
                raise GroupNotFound(message=f"{result.id} not found in db")

            group = session.query(Group).filter(Group.id == result.id).one_or_none()
            session.expunge(group)
        return group
