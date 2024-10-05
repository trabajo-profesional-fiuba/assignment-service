from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Table, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, relationship
from typing import List

from src.api.users.models import User
from src.config.database.base import Base


# One to Many association table
association_table = Table(
    "groups_students",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id", ondelete="CASCADE")),
    Column("student_id", ForeignKey("users.id"), primary_key=True),
)


class Group(Base):
    """
    Schema of a group for a table in the database
    it contains the necessary fields and relationships that
    a group needs to have, for example, its topic, the id which the group
    belongs, etc.
    """

    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    assigned_topic_id = Column(
        Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True
    )
    tutor_period_id = Column(
        Integer,
        ForeignKey("tutor_periods.id", ondelete="SET NULL"),
        nullable=True,
    )
    pre_report_date = Column(DateTime(timezone=False))
    pre_report_approved = Column(Boolean, default=False)
    pre_report_title = Column(String(100))
    intermediate_assigment_date = Column(DateTime(timezone=False))
    intermediate_assigment_approved = Column(Boolean, default=False)
    final_report_approved = Column(Boolean, default=False)
    final_report_title = Column(String(100))
    final_report_date = Column(DateTime(timezone=False))
    exhibition_date = Column(DateTime(timezone=False))
    """ postgresql.ARRAY is a dialect specif datatype for postgres sql
        if in the future the db changes, this should be refactored using a
        different approach.
        This field is supposed to contain 3 ids topics ids. No foreing key is
        needed as these keys will no be used for join operations so is better
        to skip the relationship config.
    """
    preferred_topics = Column(postgresql.ARRAY(Integer, dimensions=1), default=[])
    period_id = Column(String, ForeignKey("periods.id"))
    reviewer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    students: Mapped[List[User]] = relationship(
        secondary=association_table, lazy="subquery"
    )
    topic = relationship("Topic", back_populates="groups", lazy="noload")
    tutor_period = relationship("TutorPeriod", back_populates="groups", lazy="noload")
    period = relationship("Period", back_populates="groups", lazy="noload")