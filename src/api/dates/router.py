from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.api.auth.dependencies import authorization
from src.api.auth.jwt import InvalidJwt
from src.api.auth.service import AuthenticationService
from src.api.dates.exceptions import InvalidDate
from src.api.dates.repository import DateSlotRepository
from src.api.dates.schemas import DateSlotRequestList, DateSlotResponseList
from src.api.dates.service import DateSlotsService
from src.api.exceptions import ServerError
from src.api.groups.repository import GroupRepository
from src.api.periods.repository import PeriodRepository
from src.api.periods.service import PeriodService
from src.api.users.exceptions import InvalidCredentials
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/dates", tags=["Dates"])


@router.post(
    "/",
    response_model=DateSlotResponseList,
    summary="Creates a new list of slots",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully created slots."},
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
async def add_dates(
    slots: DateSlotRequestList,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Agrega los slots disponibles en un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_only_admin(authorization['token'])

        service = DateSlotsService(DateSlotRepository(session))
        slots_added = service.add_slots(slots, period)

        res = DateSlotResponseList.model_validate(slots_added)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)

    except InvalidDate as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.post(
    "/groups",
    response_model=DateSlotResponseList,
    summary="Creates a new list of slots for the groups",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully created slots."},
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
async def add_groups_dates(
    slots: DateSlotRequestList,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    group_id: int = Query(...),
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Agrega los slots seleccionados por un grupo"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_student_in_group(authorization['token'], group_id, GroupRepository(session))

        period_service = PeriodService(PeriodRepository(session))
        period_db = period_service.get_period_by_id(period)

        if period_db.presentation_dates_available:
            service = DateSlotsService(DateSlotRepository(session))
            slots_added = service.add_group_slots(group_id, slots)

            res = DateSlotResponseList.model_validate(slots_added)
            return ResponseBuilder.build_clear_cache_response(
                res, status.HTTP_201_CREATED
            )
        else:
            raise Exception("Submit group periods is not enable")
    except InvalidDate as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.post(
    "/tutors",
    response_model=DateSlotResponseList,
    summary="Creates a new list of slots for the tutor",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully created slots."},
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
async def add_tutors_dates(
    slots: DateSlotRequestList,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Agrega los slots seleccionados por un tutor en un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        jwt = auth_service.assert_tutor_rol(authorization['token'])
        tutor_id = auth_service.get_user_id(jwt)

        period_service = PeriodService(PeriodRepository(session))
        period_db = period_service.get_period_by_id(period)

        if period_db.presentation_dates_available:
            service = DateSlotsService(DateSlotRepository(session))
            slots_added = service.add_tutor_slots(tutor_id, period, slots)

            res = DateSlotResponseList.model_validate(slots_added)
            return ResponseBuilder.build_clear_cache_response(
                res, status.HTTP_201_CREATED
            )
        else:
            raise Exception("Submit tutor periods is not enable")

    except InvalidDate as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/",
    response_model=DateSlotResponseList,
    summary="Returns a list of available slots",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully retrieve a list of available slots."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_available_slots(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Obtiene todos los slots disponibles en un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_multiple_role(authorization['token'])

        service = DateSlotsService(DateSlotRepository(session))
        slots = service.get_slots(period)
        logger.info("Retrieve all available slots.")

        res = DateSlotResponseList.model_validate(slots)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_200_OK)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.get(
    "/tutors/{tutor_id}",
    response_model=DateSlotResponseList,
    summary="Returns a list of slots by tutor id",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully retrieve a list of available slots."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_slots_by_tutor_id(
    tutor_id: int,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Obtiene todos los slots de un tutor en un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_tutor_rol(authorization['token'], tutor_id)

        service = DateSlotsService(DateSlotRepository(session))
        slots = service.get_tutors_slots_by_id(tutor_id, period)
        logger.info(f"Retrieve all slots from tutor id: {tutor_id}")

        res = DateSlotResponseList.model_validate(slots)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_200_OK)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.get(
    "/groups/{group_id}",
    response_model=DateSlotResponseList,
    summary="Returns a list of slots by group id",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully retrieve a list of available slots by group"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_slots_by_group_id(
    group_id: int,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
):
    """Obtiene todos los slots de un grupo"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_student_in_group(authorization['token'], group_id, GroupRepository(session))

        service = DateSlotsService(DateSlotRepository(session))
        slots = service.get_groups_slots_by_id(group_id)
        logger.info(f"Retrieve all slots from group id: {group_id}")

        res = DateSlotResponseList.model_validate(slots)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_200_OK)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.put(
    "/",
    response_model=DateSlotResponseList,
    summary="Updates a list of slots",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully updated slots."},
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
async def sync_date_slots(
    slots: DateSlotRequestList,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Sobre escribe los slots disponibles"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_only_admin(authorization['token'])

        service = DateSlotsService(DateSlotRepository(session))
        slots_added = service.sync_date_slots(slots, period)
        logger.info("Slots already updated")
        res = DateSlotResponseList.model_validate(slots_added)

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except InvalidDate as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.put(
    "/groups",
    response_model=DateSlotResponseList,
    summary="Updates a list of slots by group id",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully updated slots."},
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
async def sync_group_slots(
    slots: DateSlotRequestList,
    group_id: int,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Sobrescribe los slots de un grupo"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_student_in_group(authorization['token'], group_id, GroupRepository(session))

        period_service = PeriodService(PeriodRepository(session))
        period_db = period_service.get_period_by_id(period)

        if period_db.presentation_dates_available:

            service = DateSlotsService(DateSlotRepository(session))
            slots = service.sync_group_slots(slots, group_id)
            logger.info(f"Updates all slots from group id: {group_id}")

            res = DateSlotResponseList.model_validate(slots)
            return ResponseBuilder.build_clear_cache_response(
                res, status.HTTP_201_CREATED
            )
        else:
            raise Exception("Ovewrride groups periods is not enable")
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.put(
    "/tutors",
    response_model=DateSlotResponseList,
    summary="Updates a list of slots by tutor id",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully updated slots."},
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
async def sync_tutor_slots(
    slots: DateSlotRequestList,
    tutor_id: int,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Sobreescribe los slots de un tutor en un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        jwt = auth_service.assert_tutor_rol(authorization['token'])
        tutor_id = auth_service.get_user_id(jwt)

        period_service = PeriodService(PeriodRepository(session))
        period_db = period_service.get_period_by_id(period)

        if period_db.presentation_dates_available:

            service = DateSlotsService(DateSlotRepository(session))
            slots_added = service.sync_tutor_slots(slots, tutor_id, period)

            res = DateSlotResponseList.model_validate(slots_added)
            return ResponseBuilder.build_clear_cache_response(
                res, status.HTTP_201_CREATED
            )
        else:
            raise Exception("Ovewrride tutors periods is not enable")
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e
