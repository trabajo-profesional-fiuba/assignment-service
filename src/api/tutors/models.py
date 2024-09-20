from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class TutorPeriod(Base):

    __tablename__ = "tutor_periods"

    id = Column(Integer, autoincrement=True, primary_key=True)
    period_id = Column(String, ForeignKey("periods.id", ondelete="SET NULL"))
    tutor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    capacity = Column(Integer, default=0)
    is_evaluator = Column(Boolean, default=False)

    tutor = relationship("User", back_populates="tutor_periods", lazy="subquery")
    period = relationship("Period", back_populates="tutor_periods", lazy="subquery")
    topics = relationship("Topic", secondary="topics_tutor_periods", lazy="subquery")
    groups = relationship(
        "Group", back_populates="tutor_period", uselist=True, lazy="noload"
    )

    __table_args__ = (
        UniqueConstraint("period_id", "tutor_id", name="tutor_period_const"),
    )
