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
    pre_report_title = Column(String(100), nullable=True)
    intermediate_assigment_date = Column(DateTime(timezone=False))
    intermediate_assigment_approved = Column(Boolean, default=False)
    intermediate_assigment = Column(String(250), nullable=True)
    final_report_approved = Column(Boolean, default=False)
    final_report_title = Column(String(100), nullable=True)
    final_report_date = Column(DateTime(timezone=False))
    exhibition_date = Column(DateTime(timezone=False))
    """
    postgresql.ARRAY es un tipo de dato especifico del dialecto para PostgreSQL.
    Si en el futuro la base de datos cambia, esto deberia ser refactorizado usando
    un enfoque diferente.
    Este campo esta destinado a contener 3 IDs de temas. No se necesita clave foranea
    ya que estas claves no se usaran para operaciones de JOIN, por lo que es mejor
    omitir la configuracion de la relacion.
    """
    preferred_topics = Column(postgresql.ARRAY(Integer, dimensions=1), default=[])
    period_id = Column(String, ForeignKey("periods.id"))
    reviewer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    group_number = Column(Integer)

    # Relaciones de los grupos
    students: Mapped[List[User]] = relationship(
        secondary=association_table, lazy="subquery"
    )
    topic = relationship("Topic", back_populates="groups", lazy="noload")
    tutor_period = relationship("TutorPeriod", back_populates="groups", lazy="noload")
    period = relationship("Period", back_populates="groups", lazy="noload")
    group_dates_slots = relationship(
        "GroupDateSlot", back_populates="groups", lazy="noload"
    )
