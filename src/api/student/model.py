from sqlalchemy import Column, Integer
from src.config.database.base import Base


class Group(Base):

    id = Column(Integer, autoincrement=True, primary_key=True)
    
    # un grupo tiene
    # FK al cuatrimestre del profesor al que pertenece (luego del algoritmo)
    # FK al topic
    # fecha de entrega pre-informe
    # preinforme aprobado
    # fecha de entrega intermedia
    # si fue aprobada la fecha de entrega
    # fechas de exposicion disponibles (ver many to many)
    # informe aprobado
    # fecha de exposicion asignada


# las relaciones son
# User many-to-one Group (many <= 4 per group)
# Group many-to-one Topic
# Group many-to-one TutorPeriod
#  -- para mas adelante--
# Dates many-to-many Groups
