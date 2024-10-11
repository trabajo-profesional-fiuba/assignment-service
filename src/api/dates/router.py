from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from fastapi import (
    APIRouter,
    Depends,
    Response,
    UploadFile,
    status,
    Query,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.dates.exceptions import InvalidDate
from src.api.dates.repository import DateSlotRepository
from src.api.dates.schemas import DateSlotRequestList, DateSlotResponseList
from src.api.dates.service import DateSlotsService
from src.api.exceptions import EntityNotInserted, EntityNotFound, ServerError

from src.api.users.exceptions import InvalidCredentials

from src.api.utils.response_builder import ResponseBuilder

from src.config.config import api_config
from src.config.database.database import get_db


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
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

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
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    group_id: int = Query(...),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        service = DateSlotsService(DateSlotRepository(session))
        slots_added = service.add_group_slots(group_id, slots)

        res = DateSlotResponseList.model_validate(slots_added)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)

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
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        jwt = auth_service.assert_tutor_rol(token)
        tutor_id = auth_service.get_user_id(jwt)

        service = DateSlotsService(DateSlotRepository(session))
        slots_added = service.add_tutor_slots(tutor_id, period, slots)

        res = DateSlotResponseList.model_validate(slots_added)
        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)

    except InvalidDate as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
