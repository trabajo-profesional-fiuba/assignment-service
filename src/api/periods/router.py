from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.api.auth.dependencies import authorization
from src.api.auth.jwt import InvalidJwt
from src.api.auth.service import AuthenticationService
from src.api.exceptions import (
    Duplicated,
    EntityNotFound,
    ServerError,
)
from src.api.users.exceptions import InvalidCredentials
from src.api.periods.schemas import (
    PeriodResponse,
    PeriodRequest,
    PeriodList,
    UpdatePeriodRequest,
)
from src.api.periods.exceptions import InvalidPeriod
from src.api.periods.repository import PeriodRepository
from src.api.periods.service import PeriodService
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db

router = APIRouter(prefix="/periods", tags=["Periods"])


@router.post(
    "/",
    response_model=PeriodResponse,
    summary="Add a new period",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Period schema is not correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated period"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_period(
    session: Annotated[Session, Depends(get_db)],
    period: PeriodRequest,
    authorization: Annotated[dict, Depends(authorization)],
):
    """Endpoint para agregar un nuevo cuatrimestre"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_only_admin(authorization['token'])

        service = PeriodService(PeriodRepository(session))
        res = PeriodResponse.model_validate(service.add_period(period))

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (InvalidPeriod, Duplicated) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/",
    response_model=PeriodList,
    summary="Get all periods",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_periods(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    order: str = Query(pattern="^(ASC|DESC)$", default="DESC"),
):
    """Endpoint para obtener todos los cuatrimestres"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_only_admin(authorization['token'])

        service = PeriodService(PeriodRepository(session))
        res = PeriodList.model_validate(service.get_all_periods(order))

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/{period_id}",
    response_model=PeriodResponse,
    summary="Get a given period information",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_period_by_id(
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
    period_id=Path(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para obtener un cuatrimestre particular"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_multiple_role(authorization['token'])

        service = PeriodService(PeriodRepository(session))
        res = PeriodResponse.model_validate(service.get_period_by_id(period_id))

        return ResponseBuilder.build_private_cache_response(res)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.put(
    "/",
    response_model=PeriodResponse,
    summary="Update a period",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully updated period"},
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
async def update_period(
    period: UpdatePeriodRequest,
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[dict, Depends(authorization)],
):
    """Endpoint para actualizar un cuatrimestre puntual"""
    try:
        auth_service = AuthenticationService(authorization['jwt_resolver'])
        auth_service.assert_only_admin(authorization['token'])

        period_service = PeriodService(PeriodRepository(session))
        res = period_service.update(period)

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
