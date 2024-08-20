from src.config.database.base import Base

from src.api.users.models import User
from src.api.groups.models import Group, association_table
from src.api.tutors.models import Period, TutorPeriod
from src.api.forms.models import FormPreferences
from src.api.topics.models import Topic, Category
