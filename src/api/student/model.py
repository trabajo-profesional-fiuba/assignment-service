from src.config.database.base import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    # FK tutor's period
    tutor_period_id = Column(Integer, ForeignKey("tutor_periods.id"), nullable=True)
    # FK topic
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    # fecha de entrega pre-informe
    pre_report_date = Column(DateTime(timezone=False))
    # preinforme aprobado
    pre_report_approved = Column(Boolean, default=False)
    # fecha de entrega intermedia
    intermediate_assigment_date = Column(DateTime(timezone=False))
    # si fue aprobada la fecha de entrega
    intermediate_assigment_approved = Column(Boolean, default=False)
    # fechas de exposicion disponibles (ver many to many)
    # informe aprobado
    final_report_approved = Column(Boolean, default=False)
    # fecha de exposicion asignada
    exhibition_date = Column(DateTime(timezone=False))

    # TODO: ver el lazy bien
    students = relationship("User", back_populates="group")
    topic = relationship("Topic", back_populates="groups")
    tutor_period = relationship("TutorPeriod", back_populates="groups")

# las relaciones son
# User many-to-one Group (many <= 4 per group)
# Group many-to-one Topic
# Group many-to-one TutorPeriod
#  -- para mas adelante--
# Dates many-to-many Groups
