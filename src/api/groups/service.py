from src.api.exceptions import EntityNotInserted, EntityNotFound
from src.api.groups.schemas import GroupList, GroupResponse
from src.api.students.exceptions import StudentNotFound


from src.config.logging import logger


class GroupService:
    """
    The group service contains the necessary logi to performs operations
    with Groups as schemas, as entities and as ORM Objects
    """

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_assigned_group(self, ids, tutor_period_id, topic_id, period_id):
        try:
            group = self._repository.add_group(
                ids, tutor_period_id, topic_id, period_id=period_id
            )
            logger.info(f"New group with id {group.id} created")
            return GroupResponse.model_validate(group)
        except StudentNotFound as e:
            logger.error(f"Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception as err:
            logger.error(
                f"Could not insert a group with ids: {str(ids)}, topic id {topic_id}, tutor period id: {tutor_period_id} and period id: {period_id}"
            )
            logger.error(err)
            raise EntityNotInserted(
                message="Group could't be created check if params exits"
            )

    def create_basic_group(self, ids, preferred_topics=[], period_id=None):
        try:
            group = self._repository.add_group(
                ids=ids, preferred_topics=preferred_topics, period_id=period_id
            )
            return GroupResponse.model_validate(group)
        except StudentNotFound as e:
            logger.error(f"Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception:
            logger.error(f"Could not insert a group with ids: {str(ids)}")
            raise EntityNotInserted(
                message="Group could't be created check if params exits"
            )

    def create_basic_group_with_email(
        self, emails, preferred_topics=[], period_id=None
    ):
        try:
            group = self._repository.add_group_having_emails(
                emails=emails, preferred_topics=preferred_topics, period_id=period_id
            )
            return GroupResponse.model_validate(group)
        except StudentNotFound as e:
            logger.error(f"Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception as e:
            logger.error(f"Could not insert a group with email: {str(emails)}")
            raise EntityNotInserted(
                message="Group could't be created check if params exits"
            )

    def get_groups(self, period: str):
        logger.info("Fetching all groups")
        groups = self._repository.get_groups(period)
        return GroupList.model_validate(groups)

    def create_basic_groups(self, group_result, period_id):
        for group in group_result:
            topics = group.get_topic_ids()
            emails = group.students
            self.create_basic_group_with_email(emails, topics, period_id)
