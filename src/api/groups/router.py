from typing_extensions import Annotated

from fastapi import APIRouter, Depends, status, Query

from sqlalchemy.orm import Session

from src.api.exceptions import EntityNotInserted, EntityNotFound, ServerError
from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import GroupRequest, GroupResponse
from src.api.groups.service import GroupService
from src.api.topic.repository import TopicRepository
from src.api.topic.service import TopicService
from src.api.tutors.repository import TutorRepository
from src.api.tutors.service import TutorService
from src.config.database.database import get_db

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Creates a new group",
    description="""This endpoint is intended to use for those cases which the group of
    students already have a tutor and a topic""",
)
async def add_group(
    group: GroupRequest,
    session: Annotated[Session, Depends(get_db)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        tutor_service = TutorService(TutorRepository(session))
        topic_service = TopicService(TopicRepository(session))
        group_service = GroupService(GroupRepository(session))

        tutor_period = tutor_service.get_tutor_period_by_email(
            period, group.tutor_email
        )
        topic = topic_service.get_or_add_topic(group.topic)

        return group_service.create_assigned_group(
            group.students_ids, tutor_period.id, topic.id
        )
    except (EntityNotInserted,EntityNotFound) as e:
        raise e
    except Exception:
        raise ServerError(message=str(e))
