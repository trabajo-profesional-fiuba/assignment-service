from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status, Query

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.users.schemas import UserList
from src.api.users.repository import UserRepository

from src.api.student.service import StudentService
from src.api.student.repository import StudentRepository
from src.api.student.exceptions import (
    StudentNotFound,
    StudentDuplicated,
    InvalidStudentCsv,
)

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
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="CSV file must be provided",
            )
        logger.info("csv contains the correct content-type")
        content = (await file.read()).decode("utf-8")
        service = StudentService(UserRepository(session))
        return service.create_students_from_string(content, hasher)
    except (InvalidStudentCsv, StudentDuplicated) as e:
        raise HTTPException(
            status_code=e.status_code(),
            detail=str(e),
        )
    except HTTPException as e:
        raise e
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err,
        )


@router.get(
    "/",
    response_model=UserList,
    description="Returns list of students based on user_ids",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Uid is not present inside the database"
        },
        status.HTTP_409_CONFLICT: {"description": "There are user_ids duplicated"},
    },
)
async def get_students_by_ids(
    session: Annotated[Session, Depends(get_db)],
    user_ids: list[int] = Query(default=[]),
):
    try:
        service = StudentService(StudentRepository(session))
        res = service.get_students_by_ids(user_ids)
        return res
    except StudentNotFound as st:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(st))
    except StudentDuplicated as std:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(std))
