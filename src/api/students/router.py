from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from fastapi import APIRouter, UploadFile, Depends, status, Query
from sqlalchemy.orm import Session

from src.api.auth.hasher import get_hasher, ShaHasher
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService

from src.api.exceptions import Duplicated, EntityNotFound, InvalidFileType, ServerError

from src.api.students.exceptions import StudentNotFound, StudentDuplicated
from src.api.students.repository import StudentRepository
from src.api.students.service import StudentService

from src.api.users.exceptions import InvalidCredentials
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserList

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
    },
)
async def upload_csv_file(
    file: UploadFile,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        if file.content_type != "text/csv":
            raise InvalidFileType("CSV file must be provided")

        logger.info("csv contains the correct content-type")
        content = (await file.read()).decode("utf-8")
        service = StudentService(UserRepository(session))
        res = service.create_students_from_string(content, hasher)

        return res
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

        response = JSONResponse(content = res.model_dump())
        response.headers["Cache-Control"] = "private, max-age=7200"
    
        return response
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise e
