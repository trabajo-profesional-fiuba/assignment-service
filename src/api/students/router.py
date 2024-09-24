from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from fastapi import APIRouter, UploadFile, Depends, status, Query
from sqlalchemy.orm import Session

from src.api.auth.hasher import get_hasher, ShaHasher
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService

from src.api.exceptions import Duplicated, EntityNotFound, InvalidFileType, ServerError

from src.api.forms.repository import FormRepository
from src.api.groups.repository import GroupRepository
from src.api.students.repository import StudentRepository
from src.api.students.schemas import PersonalInformation, StudentRequest
from src.api.students.service import StudentService

from src.api.users.exceptions import InvalidCredentials
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserList, UserResponse

from src.api.utils.ResponseBuilder import ResponseBuilder
from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/students", tags=["Students"])


@router.post(
    "/upload",
    response_model=UserList,
    description="Creates list of students based on a csv file",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Students were created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Invalid file type"},
    },
)
async def upload_csv_file(
    file: UploadFile,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period: str = Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        if file.content_type != "text/csv":
            raise InvalidFileType("CSV file must be provided")

        logger.info("csv contains the correct content-type")
        content = (await file.read()).decode("utf-8")
        service = StudentService(StudentRepository(session))

        res = service.create_students_from_string(
            content, hasher, UserRepository(session), period
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (Duplicated, InvalidFileType, EntityNotFound) as e:
        logger.error(f"Error while uploading csv, message: {str(e)}")
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/",
    response_model=UserList,
    description="Returns list of students based on user_ids",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Uid is not present inside the database"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "There are user_ids duplicated"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_students_by_ids(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    user_ids: list[int] = Query(default=[]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        service = StudentService(StudentRepository(session))
        res = service.get_students_by_ids(user_ids)
        logger.info("Retrieve all students by ids.")

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.get(
    "/info/me",
    response_model=PersonalInformation,
    description="Returns students info based on token",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Id is not present inside the database"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_student_info(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)
        id = auth_service.get_user_id(token)

        service = StudentService(StudentRepository(session))
        res = service.get_personal_info_by_id(
            id,
            FormRepository(session),
            UserRepository(session),
            GroupRepository(session),
            StudentRepository(session),
        )

        logger.info("Retrieve student info by id.")

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e


@router.post(
    "",
    response_model=UserResponse,
    description="Creates a new student",
    summary="Add a new student",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Student schema is not correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated student"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_student(
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    student: StudentRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = StudentService(StudentRepository(session))

        res = UserResponse.model_validate(
            service.add_student(student, hasher, UserRepository(session))
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except Duplicated as e:
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))
