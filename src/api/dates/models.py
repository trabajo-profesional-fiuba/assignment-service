from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean, CHAR
from sqlalchemy.orm import relationship

from src.config.database.base import Base


class DateSlot(Base):
    __tablename__ = "dates_slots"

    period_id = Column(String, ForeignKey("periods.id", ondelete="CASCADE"))
    slot = Column(DateTime(timezone=False), primary_key=True)
    assigned = Column(Boolean, default=False)

    # relationships
    period = relationship("Period", back_populates="dates_slots", lazy="noload")
    group_dates_slots = relationship(
        "GroupDateSlot", back_populates="dates_slots", lazy="noload"
    )
    tutor_dates_slots = relationship(
        "TutorDateSlot", back_populates="dates_slots", lazy="noload"
    )


class GroupDateSlot(Base):
    __tablename__ = "group_dates_slots"

    group_id = Column(
        Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True
    )
    slot = Column(
        DateTime(timezone=False),
        ForeignKey("dates_slots.slot", ondelete="CASCADE"),
        primary_key=True,
    )

    # relationships
    groups = relationship("Group", back_populates="group_dates_slots", lazy="noload")
    dates_slots = relationship(
        "DateSlot", back_populates="group_dates_slots", lazy="noload"
    )


class TutorDateSlot(Base):
    __tablename__ = "tutors_dates_slots"

    tutor_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    slot = Column(
        DateTime(timezone=False),
        ForeignKey("dates_slots.slot", ondelete="CASCADE"),
        primary_key=True,
    )
    period_id = Column(String, ForeignKey("periods.id", ondelete="CASCADE"))
    assigned = Column(Boolean, default=False)
    tutor_or_evaluator = Column(String,nullable=True)

    # relationships
    tutors = relationship("User", back_populates="tutor_dates_slots", lazy="noload")
    dates_slots = relationship(
        "DateSlot", back_populates="tutor_dates_slots", lazy="noload"
    )
    period = relationship("Period", back_populates="tutor_dates_slots", lazy="noload")
