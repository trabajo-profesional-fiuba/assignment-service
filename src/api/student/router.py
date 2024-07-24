from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status, Query

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.student.schemas import StudentBase
from src.api.student.service import StudentService
from src.api.student.repository import StudentRepository
from src.api.student.exceptions import StudentNotFound, StudentDuplicated,InvalidStudentCsv

from src.api.auth.hasher import get_hasher, ShaHasher
from src.config.database import get_db
from src.config.logging import logger


router = APIRouter(prefix="/students", tags=["students"])


@router.post(
    "/upload",
    response_model=list[StudentBase],
    description="Creates list of students based on a csv file",
    status_code=status.HTTP_201_CREATED,
)
async def upload_csv_file(
    file: UploadFile,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        # Check if content-type is a text/csv
        if file.content_type != "text/csv":
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="CSV file must be provided",
            )
        logger.info("csv contains the correct content-type")
        content = (await file.read()).decode("utf-8")
        service = StudentService(StudentRepository(session))
        res = service.create_students_from_string(content, hasher)

        return res
    except (InvalidStudentCsv, StudentDuplicated) as e:
        raise HTTPException(
                status_code=e.status_code(),
                detail=str(e),
    )
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading csv file.",
    )


@router.get(
    "/",
    response_model=list[StudentBase],
    description="Returns list of students based on uids",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {'description': "Uid is not present inside the database"},
        status.HTTP_409_CONFLICT: {'description': "There are uids duplicated"}
    })
async def get_students_by_ids(
    session: Annotated[Session, Depends(get_db)],
    uids: list[int] = Query(...),
):
    try:
        service = StudentService(StudentRepository(session))
        res = service.get_students_by_ids(uids)
        return res
    except StudentNotFound as st:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(st)
    )
    except StudentDuplicated as std:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(std)
    )