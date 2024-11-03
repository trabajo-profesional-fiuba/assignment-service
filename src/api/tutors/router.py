from fastapi import APIRouter, Response, UploadFile, Depends, status, Query, Path
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.service import AuthenticationService
from src.api.dates.mapper import DateSlotsMapper
from src.api.dates.repository import DateSlotRepository
from src.api.dates.schemas import DateSlotResponse, DateSlotResponseList
from src.api.exceptions import (
    Duplicated,
    EntityNotFound,
    InvalidCsv,
    InvalidFileType,
    ServerError,
)
from src.api.groups.dependencies import get_email_sender
from src.api.groups.mapper import GroupMapper
from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import GroupList
from src.api.tutors.mapper import TutorMapper
from src.api.tutors.service import TutorService
from src.api.users.exceptions import InvalidCredentials
from src.api.tutors.schemas import (
    TutorAssignedDates,
    TutorMessage,
    TutorRequest,
    TutorResponse,
    TutorList,
    TutorWithTopicsList,
)
from src.api.auth.hasher import get_hasher, ShaHasher
from src.api.auth.schemas import oauth2_scheme
from src.api.tutors.repository import TutorRepository
from src.api.users.models import Role
from src.api.users.repository import UserRepository
from src.api.users.service import UserService
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db

router = APIRouter(prefix="/tutors")


@router.post(
    "/upload",
    response_model=TutorList,
    summary="Creates list of tutors based on a csv file",
    tags=["Tutors"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "The columns are not correct"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated tutor"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
            "description": "Content-Type is not correct."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def upload_csv_file(
    file: UploadFile,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period: str = Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para cargar tutores a partir de un archivo csv"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        # Check if content-type is a text/csv
        if file.content_type != "text/csv":
            raise InvalidFileType("CSV file must be provided")
        content = (await file.read()).decode("utf-8")
        service = TutorService(TutorRepository(session))
        res = TutorList.model_validate(
            service.create_tutors_from_csv(
                content, period, hasher, UserRepository(session)
            )
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (InvalidCsv, EntityNotFound, Duplicated, InvalidFileType) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.post(
    "",
    response_model=TutorResponse,
    summary="Add a new tutor",
    tags=["Tutors"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Tutor schema is not correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated tutor"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_tutor(
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    tutor: TutorRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    """Endpoint para agregar un tutor manualmente"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = TutorService(TutorRepository(session))
        res = TutorResponse.model_validate(
            service.add_tutor(tutor, hasher, UserRepository(session))
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except Duplicated as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.delete(
    "/{tutor_id}",
    summary="Deletes a tutor based on its id.",
    tags=["Tutors"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Tutor id not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_tutor(
    tutor_id: int,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    """Endpoint para borrar un tutor"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        service = TutorService(TutorRepository(session))
        res = service.delete_tutor(tutor_id)

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_202_ACCEPTED)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.post(
    "/{tutor_id}/periods",
    response_model=TutorResponse,
    summary="Add new period",
    tags=["Tutors"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Tutor not found"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated period"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_period_to_tutor(
    session: Annotated[Session, Depends(get_db)],
    tutor_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id: str = Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para asignar un nuevo cuatrimestre a un tutor"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = TutorService(TutorRepository(session))
        res = TutorResponse.model_validate(
            service.add_period_to_tutor(tutor_id, period_id)
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (Duplicated, EntityNotFound) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/{tutor_id}/periods",
    response_model=TutorResponse,
    summary="Get all periods of tutor_id",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Tutor not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_tutor_periods(
    session: Annotated[Session, Depends(get_db)],
    tutor_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    """Endpoint para obtener todos los cuatrimestre en el que un tutor tutorea"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)

        user_id = auth_service.get_user_id(token)
        user_service = UserService(UserRepository(session))
        user = user_service.get_user_by_id(user_id)
        if user.role == Role.TUTOR:
            user_service.validate_tutor(tutor_id, user)

        service = TutorService(TutorRepository(session))
        response = TutorResponse.model_validate(
            service.get_periods_by_tutor_id(tutor_id)
        )
        return ResponseBuilder.build_private_cache_response(response)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/periods/{period_id}",
    response_model=TutorWithTopicsList,
    summary="Get all the tutors with their topics based on a period",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_tutors_by_period_id(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Path(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para obtener los tutores de un cuatrimestre"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = TutorService(TutorRepository(session))

        res = TutorWithTopicsList.model_validate(
            service.get_tutors_by_period_id(period_id)
        )

        return ResponseBuilder.build_private_cache_response(res)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/my-groups",
    response_model=GroupList,
    summary="Get all the groups of a tutor based on a period",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_groups_by_tutor(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para obtener los grupos de un cuatrimestre del cual uno es tutor"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)
        tutor_id = auth_service.get_user_id(token)

        service = TutorService(TutorRepository(session))
        group_repository = GroupRepository(session)

        groups = GroupList.model_validate(
            service.get_groups_from_tutor_id(tutor_id, period_id, group_repository)
        )

        return ResponseBuilder.build_private_cache_response(groups)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/reviewer/my-groups",
    response_model=GroupList,
    summary="Get all the groups of a tutor based on a period",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_groups_by_reviewer_id(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para obtener los grupos de un cuatrimestre del cual uno es revisor"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)
        tutor_id = auth_service.get_user_id(token)

        service = TutorService(TutorRepository(session))
        group_repository = GroupRepository(session)

        groups = GroupList.model_validate(
            service.get_groups_from_reviewer_id(tutor_id, period_id, group_repository)
        )

        return ResponseBuilder.build_private_cache_response(groups)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.post(
    "/notify-group",
    summary="Sends to students and tutor the email notification",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def notify_students(
    body: TutorMessage,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    email_sender: Annotated[object, Depends(get_email_sender)],
    group_id: int = Query(...),
):
    """Endpoint para enviar un mail al grupo de estudiantes"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)
        tutor_id = auth_service.get_user_id(token)

        service = TutorService(TutorRepository(session))
        group_repository = GroupRepository(session)

        group_mapper = GroupMapper()
        group = group_mapper.map_model_to_assigned_group(
            group_repository.get_group_by_id(
                group_id,
                load_topic=True,
                load_period=False,
                load_students=True,
                load_tutor=True,
            )
        )

        response = service.notify_students(tutor_id, group, email_sender, body.body)
        if response == 202:
            return "Emails sent succesfully"
        else:
            raise Exception("Something happend while sending emails")
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/assigned-dates",
    response_model=TutorAssignedDates,
    summary="Get all the assgined of a tutor based on a period",
    tags=["Tutors"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_404_NOT_FOUND: {"description": "Period not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def assigned_dates(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Endpoint para obtener los grupos de un cuatrimestre del cual uno es revisor"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)
        tutor_id = auth_service.get_user_id(token)

        service = TutorService(TutorRepository(session))
        dates = service.get_assigned_dates(
            period_id, tutor_id, DateSlotRepository(session)
        )

        tutor_dates = [
            DateSlotResponse(slot=row[0].slot, group_number=row[1], topic=row[2])
            for row in dates[0]
        ]
        evaluator_dates = [
            DateSlotResponse(slot=row[0].slot, group_number=row[1], topic=row[2])
            for row in dates[1]
        ]

        return TutorAssignedDates(
            tutor_dates=tutor_dates, evaluator_dates=evaluator_dates
        )
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.post(
    "/evaluator",
    summary="Make a tutor an evaluator for one tutor period",
    tags=["Tutors"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated tutor"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_202_ACCEPTED,
)
async def make_evaluator(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
    tutor_id: int = Query(...),
):
    """Endpoint para agregar un tutor manualmente"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        service = TutorService(TutorRepository(session))
        service.make_evaluator(period_id, tutor_id)

        return Response(status_code=status.HTTP_202_ACCEPTED)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))
