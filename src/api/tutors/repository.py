from sqlalchemy.orm import Session
from sqlalchemy import exc

from src.api.users.schemas import UserResponse
from src.api.users.model import User, Role
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess
