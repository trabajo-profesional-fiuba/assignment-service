from sqlalchemy.dialects import postgresql
from typing import List
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from src.api.users.model import User
from src.config.database.base import Base


# Many to Many association table
association_table = Table(
    "groups_students",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
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
    assigned_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    tutor_period_id = Column(Integer, ForeignKey("tutor_periods.id"), nullable=True)
    pre_report_date = Column(DateTime(timezone=False))
    pre_report_approved = Column(Boolean, default=False)
    intermediate_assigment_date = Column(DateTime(timezone=False))
    intermediate_assigment_approved = Column(Boolean, default=False)
    final_report_approved = Column(Boolean, default=False)
    exhibition_date = Column(DateTime(timezone=False))
    prefered_topics = Column(postgresql.ARRAY(Integer, dimensions=1),default=[])

    # TODO: ver el lazy bien
    students: Mapped[List[User]] = relationship(secondary=association_table, lazy="joined")
    topic = relationship("Topic", back_populates="groups",lazy="joined")
    tutor_period = relationship("TutorPeriod", back_populates="groups",lazy="joined")