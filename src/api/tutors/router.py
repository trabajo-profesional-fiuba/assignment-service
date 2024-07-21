from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.tutors.schemas import Tutor
from src.api.tutors.service import TutorService
from src.api.tutors.repository import TutorRepository
from src.api.auth.hasher import get_hasher, ShaHasher
from src.config.database import get_db

router = APIRouter(prefix="/tutors", tags=["tutors"])


@router.post(
    "/upload",
    response_model=list[Tutor],
    description="Creates list of tutors based on a csv file",
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
        service = TutorService(TutorRepository(session))
        res = service.create_tutors_from_string(content, hasher)

        return res
    except HTTPException as e:
        raise e
