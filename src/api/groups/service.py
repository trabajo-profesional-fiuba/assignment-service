import datetime

from src.api.exceptions import EntityNotInserted, EntityNotFound
from src.api.groups.exceptions import GroupNotFound
from src.api.groups.schemas import BlobDetails
from src.api.students.exceptions import StudentNotFound
from src.config.logging import logger


class GroupService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_assigned_group(self, ids, tutor_period_id, topic_id, period_id):
        """Crea un grupo que tiene ya tema y tutor"""
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
        """Crea un grupo sin tema y tutor con temas de preferencias"""
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
        """Crea un grupo sin tema y tutor con temas de preferencias a partir de los emails de los alumnos"""
        try:
            group = self._repository.add_group_having_emails(
                emails=emails, preferred_topics=preferred_topics, period_id=period_id
            )
            return group
        except StudentNotFound as e:
            logger.error("Could not insert a group because some ids are not valid")
            raise EntityNotFound(message=str(e))
        except Exception:
            logger.error(f"Could not insert a group with email: {str(emails)}")
            raise EntityNotInserted(
                message="Group could't be created check if params exits"
            )

    def get_groups(
        self,
        period: str,
        load_topic: bool = False,
        load_tutor_period: bool = False,
        load_period: bool = False,
        load_students: bool = False,
        load_dates: bool = False,
    ):
        """Obtiene todos los grupos de un cuatrimestre"""
        logger.info("Fetching all groups")
        groups = self._repository.get_groups(
            period,
            load_topic,
            load_tutor_period,
            load_period,
            load_students,
            load_dates,
        )
        return groups

    def create_basic_groups(self, group_result, period_id):
        """Crea una lista de grupos sin temas ni tutores"""
        for group in group_result:
            topics = group.get_topic_ids()
            emails = group.students
            self.create_basic_group_with_email(emails, topics, period_id)

    def get_goups_without_tutor_and_topic(self):
        """Obtiene todos los grupos sin tutor ni tema asignado"""
        db_groups = self._repository.get_groups_without_tutor_and_period()
        return db_groups

    def update(self, groups, period):
        """Actualiza los grupos de un cuatrimestre especifico"""
        try:
            for group in groups:
                attributes = group.model_dump(exclude_unset=True)
                attributes.pop("id", None)

                self._repository.update(group.id, attributes)

            return self._repository.get_groups(period=period, load_topic=True)
        except Exception as e:
            logger.error(f"Could not update groups because of: {str(e)}")
            raise EntityNotInserted(
                message="Group could't be updated due a database problem. Check if the\
                id provided are correct."
            )

    def upload_initial_project(
        self, group_id: int, project_title: str, data: bytes, storage_client
    ):
        """Sube el anteproyecto de un grupo a Azure Storage"""
        try:
            group = self._repository.get_group_by_id(group_id)
            path = f"{group.period_id}/{group.id}/anteproyecto.pdf"
            blob = storage_client.upload(data=data, filename=path, overwrite=True)
            self._repository.update(
                group_id,
                {
                    "pre_report_date": datetime.datetime.now(),
                    "pre_report_title": project_title,
                },
            )

            return blob
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def upload_final_project(
        self, group_id: int, project_title: str, data: bytes, storage_client
    ):
        """Sube el proyecto final de un grupo a Azure Storage"""
        try:
            group = self._repository.get_group_by_id(group_id)
            path = f"{group.period_id}/{group.id}/informe-final.pdf"
            blob = storage_client.upload(data=data, filename=path, overwrite=True)
            self._repository.update(
                group_id,
                {
                    "final_report_date": datetime.datetime.now(),
                    "final_report_title": project_title,
                },
            )

            return blob
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def upload_intermediate_project(self, group_id: int, link: str):
        """Updatea el proyecto intermedio (link a yt) de un grupo"""
        try:
            group = self._repository.get_group_by_id(group_id)
            self._repository.update(
                group.id,
                {
                    "intermediate_assigment_date": datetime.datetime.now(),
                    "intermediate_assigment": link,
                },
            )
            return link
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def download_final_project(self, period: str, group_id: int, storage_client):
        """Descarga el proyecto final de uun grupo"""
        try:
            path = f"{period}/{group_id}/informe-final.pdf"
            file_as_bytes = storage_client.download(path)
            return file_as_bytes
        except Exception as e:
            logger.error(f"Could not download {path}")
            raise e

    def download_initial_project(self, period: str, group_id: int, storage_client):
        """Descarga el anteproyecto de uun grupo"""
        try:
            path = f"{period}/{group_id}/anteproyecto.pdf"
            file_as_bytes = storage_client.download(path)
            return file_as_bytes
        except Exception as e:
            logger.error(f"Could not download {path}")
            raise e

    def list_initial_project(self, period, storage_client):
        """Lista los anteproyectos"""
        pattern = f"^{period}\\/[0-9]+\\/anteproyecto\\.pdf$"
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

    def list_final_project(self, period, storage_client):
        """Lista los proyectos finales"""
        pattern = f"^{period}\\/[0-9]+\\/informe-final\\.pdf$"
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

    def get_group_by_id(
        self, group_id: int, load_students: bool = False, load_tutor=False
    ):
        """Obtiene un grupo por id"""
        try:
            logger.info(f"Fetching group: {group_id}")
            group = self._repository.get_group_by_id(
                group_id=group_id, load_students=load_students, load_tutor=load_tutor
            )
            return group
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def get_group_by_student_id(self, student_id: int):
        try:
            """Obtiene el grupo donde esta el alumno"""
            logger.info(f"Fetching group for student : {student_id}")
            group = self._repository.get_group_by_student_id(student_id)
            return group
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))

    def assign_date(self,group_id:int, date: datetime):
        """ Asigna una fecha a un grupo"""
        try:
            self._repository.update(
                group_id,
                {
                    "exhibition_date": date,
                },
            )
        except GroupNotFound as e:
            logger.error(f"Could not found group because of: {str(e)}")
            raise EntityNotFound(message=str(e))
