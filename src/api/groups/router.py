from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Union

from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.exceptions import EntityNotInserted, EntityNotFound, ServerError

from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import (
    GroupList,
    GroupResponse,
    GroupWithPreferredTopicsRequest,
    GroupWithTutorTopicRequest,
)
from src.api.groups.service import GroupService


from src.api.topics.repository import TopicRepository
from src.api.topics.service import TopicService
from src.api.tutors.repository import TutorRepository
from src.api.tutors.service import TutorService
from src.api.users.exceptions import InvalidCredentials

from src.config.database.database import get_db

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post(
    "/",
    response_model=GroupResponse,
    summary="Creates a new group",
    description="""This endpoint creates a new group. The group can already have \
    tutor and topic or just preferred topics.""",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added a new group."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a \
            client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_group(
    group: GroupWithTutorTopicRequest,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        tutor_service = TutorService(TutorRepository(session))
        topic_service = TopicService(TopicRepository(session))
        group_service = GroupService(GroupRepository(session))

        tutor_period = tutor_service.get_tutor_period_by_tutor_email(
            period, group.tutor_email
        )
        topic = topic_service.get_or_add_topic(group.topic)

        return GroupResponse.model_validate(
            group_service.create_assigned_group(
                group.students_ids, tutor_period.id, topic.id, period_id=period
            )
        )
    except (EntityNotInserted, EntityNotFound) as e:
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/",
    response_model=GroupList,
    summary="Returns the list of groups that are in a specific period",
    responses={
        status.HTTP_200_OK: {"description": "Successfully added a new group."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_groups(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        group_service = GroupService(GroupRepository(session))

        return GroupList.model_validate(group_service.get_groups(period))
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
