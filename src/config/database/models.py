"""
Cada vez que se agregue un nuevo modelo al sistema
debe agregarse en este archivo.

Dado que este archivo es el que tiene el trackeo de todas las tablas
que estan relacionadas con Base.

Evitando que no haya tablas sin construir
"""

from src.config.database.base import Base

from src.api.users.models import User
from src.api.groups.models import Group, association_table
from src.api.periods.models import Period
from src.api.tutors.models import TutorPeriod
from src.api.forms.models import FormPreferences
from src.api.topics.models import Topic, Category
from src.api.students.models import StudentPeriod
from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot
