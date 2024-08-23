from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status, Query

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.exceptions import Duplicated, EntityNotFound, InvalidFileType, ServerError
from src.api.users.schemas import UserList
from src.api.users.repository import UserRepository

from src.api.students.service import StudentService
from src.api.students.repository import StudentRepository
from src.api.students.exceptions import StudentNotFound, StudentDuplicated

from src.api.auth.hasher import get_hasher, ShaHasher
from src.config.database.database import get_db
from src.config.logging import logger


router = APIRouter(prefix="/students", tags=["Students"])


@router.post(
    "/upload",
    response_model=UserList,
    description="Creates list of students based on a csv file",
    status_code=status.HTTP_201_CREATED,
)
async def upload_csv_file(
    file: UploadFile,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
):
    try:
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
        status.HTTP_409_CONFLICT: {"description": "There are user_ids duplicated"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_students_by_ids(
    session: Annotated[Session, Depends(get_db)],
    user_ids: list[int] = Query(default=[]),
):
    service = StudentService(StudentRepository(session))
    res = service.get_students_by_ids(user_ids)
    logger.info("Retrieve all students by ids.")

    return res