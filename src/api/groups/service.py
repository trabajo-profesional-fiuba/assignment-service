import datetime

from src.api.exceptions import EntityNotInserted, EntityNotFound
from src.api.groups.exceptions import GroupNotFound
from src.api.groups.schemas import BlobDetails
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
            return group
        except StudentNotFound as e:
            logger.error("Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception as err:
            logger.error(
                f"Could not insert a group with ids: {str(ids)}, topic id {topic_id}, \
                tutor period id: {tutor_period_id} and period id: {period_id}"
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
            return group
        except StudentNotFound as e:
            logger.error("Could not insert a group because some ids are not valid")
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
            return group
        except StudentNotFound as e:
            logger.error("Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception as e:
            logger.error(f"Could not insert a group with email: {str(emails)}")
            raise EntityNotInserted(
                message="Group could't be created check if params exits"
            )

    def get_groups(self, period: str):
        logger.info("Fetching all groups")
        groups = self._repository.get_groups(period)
        return groups

    def create_basic_groups(self, group_result, period_id):
        for group in group_result:
            topics = group.get_topic_ids()
            emails = group.students
            self.create_basic_group_with_email(emails, topics, period_id)

    def get_goups_without_tutor_and_topic(self):
        db_groups = self._repository.get_groups_without_tutor_and_period()
        return db_groups

    def update(self, groups, period):
        try:
            groups_to_update = list()
            for group in groups:
                # b_* comes from binding params
                groups_to_update.append(
                    {
                        "b_id": group.id,
                        "b_assigned_topic_id": group.topic_id,
                        "b_tutor_period_id": group.tutor_period_id,
                    }
                )
            self._repository.bulk_update(groups_to_update, period)
            return self._repository.get_groups(period)
        except Exception as e:
            logger.error(f"Could not update groups because of: {str(e)}")
            raise EntityNotInserted(
                message="Group could't be updated due a database problem. Check if the\
                id provided are correct."
            )

    def upload_initial_project(self, group_id: int, data: bytes, storage_client):
        try:
            group = self._repository.get_group_by_id(group_id)
            path = f"{group.period_id}/{group.id}/initial-project.pdf"
            blob = storage_client.upload(data=data, filename=path, overwrite=True)
            self._repository.update(
                group_id, {"pre_report_date": datetime.datetime.now()}
            )

            return blob
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def download_initial_project(self, period: str, group_id: int, storage_client):
        try:
            path = f"{period}/{group_id}/initial-project.pdf"
            file_as_bytes = storage_client.download(path)
            return file_as_bytes
        except Exception as e:
            logger.error(f"Could not download {path}")
            raise e

    def list_initial_project(self, period, storage_client):
        pattern = f"^{period}\\/[0-9]+\\/initial-project\\.pdf$"
        blobs = storage_client.list_blobs(prefix=period, pattern=pattern)
        blob_details_list = [
            BlobDetails(
                name=blob.name,
                created_on=blob.creation_time,
                last_modified=blob.last_modified,
                container=blob.container,
            )
            for blob in blobs
        ]
        return blob_details_list

    def get_group(
        self,
        group_id: int,
    ):
        try:
            logger.info(f"Fetching group: {group_id}")
            group = self._repository.get_group_by_id(group_id)
            return group
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def get_group_by_student_id(self, student_id: int):
        try:
            logger.info(f"Fetching group for student : {student_id}")
            group = self._repository.get_group_by_student_id(student_id)
            return group
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))
