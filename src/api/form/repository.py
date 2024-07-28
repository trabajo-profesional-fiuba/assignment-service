from sqlalchemy import exc
from sqlalchemy.orm import Session
from src.api.form.schemas import GroupFormRequest, GroupFormResponse
from src.api.form.models import GroupFormPreferences
from src.api.form.exceptions import StudentNotFound
from src.api.users.model import User, Role
from src.api.topic.models import Topic
from src.api.form.exceptions import TopicNotFound


class FormRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_group_form(self, group_form: GroupFormRequest, uids: list[int]):
        with self.Session() as session:
            with session.begin():
                db_items = []
                responses = []

                # Validate topics
                topics = [group_form.topic_1, group_form.topic_2, group_form.topic_3]
                for topic in topics:
                    if not session.query(Topic).filter_by(name=topic).first():
                        raise TopicNotFound(f"Topic '{topic}' not found.")

                # Validate students
                for uid in uids:
                    user = session.query(User).filter_by(id=uid).first()
                    if not user:
                        raise StudentNotFound(f"Student with uid '{uid}' not found.")
                    if user.rol != Role.STUDENT:
                        raise StudentNotFound(
                            "The student must have the role 'student'."
                        )

                    db_item = GroupFormPreferences(
                        uid=uid,
                        group_id=group_form.group_id,
                        topic_1=group_form.topic_1,
                        topic_2=group_form.topic_2,
                        topic_3=group_form.topic_3,
                    )
                    db_items.append(db_item)
                    responses.append(GroupFormResponse.model_validate(db_item))
                session.add_all(db_items)
                return responses
