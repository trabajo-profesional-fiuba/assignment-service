from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.config.database.base import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    pre_report_date = Column(DateTime(timezone=False))
    pre_report_approved = Column(Boolean, default=False)
    intermediate_assigment_date = Column(DateTime(timezone=False))
    intermediate_assigment_approved = Column(Boolean, default=False)
    final_report_approved = Column(Boolean, default=False)
    exhibition_date = Column(DateTime(timezone=False))

    # TODO: ver el lazy bien
    assignment = relationship(
        "GroupAssignment", back_populates="group", lazy="joined"
    )  # Fixed typo
    topic = relationship("Topic", back_populates="groups")


class GroupAssignment(Base):
    __tablename__ = "group_assignments"

    id = Column(Integer, autoincrement=True, primary_key=True)
    tutor_period_id = Column(Integer, ForeignKey("tutor_periods.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    __table_args__ = (UniqueConstraint("student_id", "group_id", "tutor_period_id"),)

    group = relationship("Group", back_populates="assignment")
    student = relationship("User", back_populates="assignment")
    tutor_period = relationship("TutorPeriod", back_populates="assignments")
