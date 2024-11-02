from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class FormPreferences(Base):
    """
    un FormPreferences es una fila que posee una respuesta individual.

    Si un grupo manda una respuesta y en ese grupo son 3 integrantes, entonces
    se generan 3 filas con topics answer_id, topic_1,2,3 repetidos y cambia el
    id y el user_id

    """

    __tablename__ = "form_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    answer_id = Column(DateTime, nullable=False)
    topic_1 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic_2 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic_3 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    period_id = Column(String, ForeignKey("periods.id", ondelete="CASCADE"))

    # Relaciones
    student = relationship("User", lazy="noload")
    period = relationship("Period", back_populates="form_preferences", lazy="noload")
