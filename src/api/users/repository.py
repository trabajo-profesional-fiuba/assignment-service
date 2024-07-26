from sqlalchemy.orm import Session


from src.api.users.model import User
from src.api.users.exceptions import UserNotFound




class UserRepository:

    def __init__(self, sess: Session):
        self.Session = sess
    
    def get_user_by_email(self, email:str):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).one_or_none()
            if not user:
                raise UserNotFound()
            
            #FIXME - Separar en schema
            return user