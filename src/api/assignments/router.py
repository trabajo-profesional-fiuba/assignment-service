from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, Query, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.assignments.service import AssignmentService
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.exceptions import ServerError

from src.api.forms.repository import FormRepository
from src.api.forms.service import FormService
from src.api.groups.mapper import GroupMapper
from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import AssignedGroupList, AssignedGroupResponse
from src.api.groups.service import GroupService

from src.api.topics.mapper import TopicMapper
from src.api.topics.repository import TopicRepository
from src.api.topics.service import TopicService
from src.api.tutors.mapper import TutorMapper
from src.api.tutors.repository import TutorRepository
from src.api.tutors.service import TutorService
from src.api.users.exceptions import InvalidCredentials

from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post(
    "/incomplete-groups",
    summary="Runs the assignment of incomplete groups",
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Successfully assigned groups"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized to perform action"
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
    status_code=status.HTTP_202_ACCEPTED,
)
async def assign_incomplete_groups(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        form_service = FormService(FormRepository(session))
        topic_repository = TopicRepository(session)
        group_service = GroupService(GroupRepository(session))

        answers = form_service.get_answers(topic_repository)
        service = AssignmentService()

        group_result = service.assignment_incomplete_groups(answers)
        group_service.create_basic_groups(group_result, period_id)
        return Response(status_code=status.HTTP_202_ACCEPTED, content="Created")
    except Exception as e:
        logger.error(str(e))
        raise ServerError("Unexpected error happend")


@router.post(
    "/group-topic-tutor",
    response_model=AssignedGroupList,
    summary="Runs the assigment of tutor and topic for grpi",
    responses={
        status.HTTP_200_OK: {"description": "Successfully assigned groups"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unkown operation"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized to perform action"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happend inside the backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def assign_incomplete_groups(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
    balance_limit: int = Query(gt=0, default=5),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        tutors_service = TutorService(TutorRepository(session))
        tutors_mapper = TutorMapper()
        tutors = tutors_mapper.convert_from_periods_to_single_period_tutors(
            tutors_service.get_tutor_periods_by_period_id(period_id)
        )

        topic_service = TopicService(TopicRepository(session))
        topic_mapper = TopicMapper()
        topics = topic_mapper.convert_from_models_to_topic(
            topic_service.get_topics_by_period(period_id)
        )

        group_service = GroupService(GroupRepository(session))
        group_mapper = GroupMapper()
        groups = group_mapper.convert_from_models_to_unassigned_groups(
            group_service.get_goups_without_tutor_and_topic(), topics
        )

        service = AssignmentService()

        assignment_result = service.assignment_group_topic_tutor(
            groups, topics, tutors, balance_limit
        )

        assignment_response = AssignedGroupList.model_validate(
            [
                AssignedGroupResponse(
                    id=assigned_group.id,
                    tutor=assigned_group.tutor_as_dict(),
                    topic=assigned_group.topic_as_dict(),
                )
                for assigned_group in assignment_result
            ]
        )

        return assignment_response
    except InvalidJwt as e:
        raise InvalidCredentials(str(e))
    except Exception as e:
        raise ServerError("error")
