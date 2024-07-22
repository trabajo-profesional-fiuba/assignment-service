from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.student.schemas import StudentBase
from src.api.student.service import StudentService
from src.api.student.repository import StudentRepository
from src.api.auth.hasher import get_hasher, ShaHasher
from src.config.database import get_db

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
        content = (await file.read()).decode("utf-8")
        service = StudentService(StudentRepository(session))
        res = service.create_students_from_string(content, hasher)

        return res
    except HTTPException as e:
        raise e
