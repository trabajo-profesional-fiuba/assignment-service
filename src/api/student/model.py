from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.config.database.base import Base


class Group(Base):
    """
    Schema of a group for a table in the database
    it contains the necessary fields and relationships that
    a group needs to have, for example, its topic, the id which the group
    belongs, etc.
    """

    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    tutor_period_id = Column(Integer, ForeignKey("tutor_periods.id"))
    pre_report_date = Column(DateTime(timezone=False))
    pre_report_approved = Column(Boolean, default=False)
    intermediate_assigment_date = Column(DateTime(timezone=False))
    intermediate_assigment_approved = Column(Boolean, default=False)
    final_report_approved = Column(Boolean, default=False)
    exhibition_date = Column(DateTime(timezone=False))

    # TODO: ver el lazy bien
    assignment = relationship("GroupAssignment", back_populates="group", lazy="joined")
    topic = relationship("Topic", back_populates="groups")
    tutor_period = relationship("TutorPeriod", back_populates="groups")


class GroupAssignment(Base):
    """
    Schema of a association between a Group and a User which needs to
    have a role of STUDENT, (It should be managed by other logic class).

    This table can only contain a unique user id, meaning  a user id cannot be
    in two different groups at the same time.
    """

    __tablename__ = "group_assignments"

    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)

    __table_args__ = (UniqueConstraint("student_id"),)

    group = relationship("Group", back_populates="assignment")
    student = relationship("User", back_populates="assignment")
