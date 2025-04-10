from fastapi import APIRouter, Depends, status, Query, Response
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.api.assignments.service import AssignmentService
from src.api.auth.dependencies import authorization
from src.api.auth.jwt import InvalidJwt
from src.api.auth.service import AuthenticationService
from src.api.dates.mapper import DateSlotsMapper
from src.api.dates.repository import DateSlotRepository
from src.api.dates.service import DateSlotsService
from src.api.exceptions import ServerError
from src.api.forms.repository import FormRepository
from src.api.forms.service import FormService
from src.api.groups.mapper import GroupMapper
from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import (
    AssignedDateResult,
    AssignedDateSlotResponse,
    AssignedDateSlotUpdate,
    AssignmentResult,
)
from src.api.groups.service import GroupService
from src.api.topics.mapper import TopicMapper
from src.api.topics.repository import TopicRepository
from src.api.topics.service import TopicService
from src.api.tutors.mapper import TutorMapper
from src.api.tutors.repository import TutorRepository
from src.api.tutors.service import TutorService
from src.api.users.exceptions import InvalidCredentials
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db
from src.config.logging import logger
from src.core.date_slots import DateSlot


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
    authorization: Annotated[dict, Depends(authorization)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint que ejecuta el algoritmo que completa aquellos grupos que no son de a 4"""
    try:
        auth_service = AuthenticationService(authorization["jwt_resolver"])
        auth_service.assert_only_admin(authorization["token"])

        form_service = FormService(FormRepository(session))
        topic_repository = TopicRepository(session)
        group_service = GroupService(GroupRepository(session))

        answers = form_service.get_answers(topic_repository, period_id)
        service = AssignmentService()

        group_result = service.assignment_incomplete_groups(answers)
        group_service.create_basic_groups(group_result, period_id)

        return Response(status_code=status.HTTP_202_ACCEPTED, content="Created")
    except Exception as e:
        logger.error(str(e))
        raise ServerError("Unexpected error happend")


@router.post(
    "/group-topic-tutor",
    response_model=AssignmentResult,
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
            "description": "Input validation has failed, typically resulting\
            in a client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened\
            inside the backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def assign_group_topic_tutor(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
    balance_limit: int = Query(gt=0, default=5),
    method: str = Query(pattern="^(lp|flow)$", default="lp"),
):
    try:
        """Ejecuta el algoritmo de grupos, temas y tutores aplicando un metodo preferido"""
        auth_service = AuthenticationService(authorization["jwt_resolver"])
        auth_service.assert_only_admin(authorization["token"])

        topic_service = TopicService(TopicRepository(session))
        topics = TopicMapper.map_models_to_topics(
            topic_service.get_topics_by_period(period_id)
        )

        tutors_service = TutorService(TutorRepository(session))
        tutors = TutorMapper.map_tutor_period_to_tutors(
            tutors_service.get_tutor_periods_by_period_id(period_id)
        )

        group_service = GroupService(GroupRepository(session))
        groups = GroupMapper.map_models_to_unassigned_groups(
            group_service.get_goups_without_tutor_and_topic(), topics
        )

        service = AssignmentService()
        assignment_result = service.assignment_group_topic_tutor(
            groups, topics, tutors, balance_limit, method
        )

        return ResponseBuilder.build_clear_cache_response(
            assignment_result.to_json(), status.HTTP_200_OK
        )
    except InvalidJwt as e:
        raise InvalidCredentials(str(e))
    except Exception as e:
        raise ServerError(str(e))


@router.post(
    "/date-assigment",
    response_model=AssignedDateResult,
    summary="Runs the assignment of assignment dates",
    responses={
        status.HTTP_200_OK: {"description": "Successfully assigned dates"},
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
async def assign_dates(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period_id: str = Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
    max_groups_per_week: int = Query(default=5, gt=0),
    max_dif_evaluators: int = Query(default=5, gt=0),
):
    try:
        """Resuelve el algoritmo de fechas y grupos"""
        auth_service = AuthenticationService(authorization["jwt_resolver"])
        auth_service.assert_only_admin(authorization["token"])

        dates_service = DateSlotsService(DateSlotRepository(session))
        available_dates = DateSlotsMapper.map_models_to_date_slots(
            dates_service.get_slots(period_id, only_available=True)
        )

        tutors_service = TutorService(TutorRepository(session))
        tutors_mapper = TutorMapper()
        tutors = tutors_mapper.map_models_to_tutors(
            tutors_service.get_tutors_with_dates(period_id)
        )
        evaluators = tutors_mapper.map_models_to_tutors(
            tutors_service.get_evaluators_with_dates(period_id)
        )

        group_service = GroupService(GroupRepository(session))
        groups = GroupMapper.map_models_to_assigned_groups(
            group_service.get_groups(
                period=period_id, load_tutor_period=True, load_dates=True
            ),
        )

        service = AssignmentService()
        assignment_result = service.assignment_dates(
            available_dates,
            tutors,
            evaluators,
            groups,
            max_groups_per_week,
            max_dif_evaluators,
        )

        return ResponseBuilder.build_clear_cache_response(
            assignment_result.to_json(), status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(str(e))
        raise ServerError("Unexpected error happend")


@router.put(
    "/date-assigment",
    summary="Updates dates relationships",
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Successfully updated dates"},
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
async def update_assignments(
    assignments: list[AssignedDateSlotUpdate],
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        """Upsertea los resultados para marcarlos como asignados"""
        auth_service = AuthenticationService(authorization["jwt_resolver"])
        auth_service.assert_only_admin(authorization["token"])

        dates_service = DateSlotsService(DateSlotRepository(session))
        group_service = GroupService(GroupRepository(session))

        for assignment in assignments:
            date = assignment.date
            evaluator_id = assignment.evaluator_id
            tutor_id = assignment.tutor_id
            group_id = assignment.group_id

            dates_service.assign_date(date, tutor_id, evaluator_id, group_id, period_id)
            group_service.assign_date(group_id, date)

        return Response(status_code=status.HTTP_202_ACCEPTED)
    except Exception as e:
        logger.error(str(e))
        raise ServerError("Unexpected error happend")


@router.get(
    "/date-assigment",
    response_model=list[AssignedDateSlotResponse],
    summary="Runs all the assignments dates",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returns all the asignment date"
        },
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
    status_code=status.HTTP_200_OK,
)
async def get_assigned_dates(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        """Devuelve el resultado del algoritmo en un cuatrimestre dado"""
        auth_service = AuthenticationService(authorization["jwt_resolver"])
        auth_service.assert_only_admin(authorization["token"])

        dates_service = DateSlotsService(DateSlotRepository(session))
        assigned_dates = dates_service.get_assigned_dates(period_id)
        assignments = list()
        for assigned_date in assigned_dates:
            date = DateSlot(assigned_date[0])
            assignments.append(
                AssignedDateSlotResponse(
                    group_id=assigned_date[3],
                    group_number=assigned_date[4],
                    tutor_id=assigned_date[2],
                    evaluator_id=assigned_date[1],
                    date=date.date,
                    spanish_date=date.get_spanish_date(),
                )
            )
        return assignments
    except Exception as e:
        logger.error(str(e))
        raise ServerError("Unexpected error happend")
