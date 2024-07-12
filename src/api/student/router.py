from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends
from fastapi.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException


from src.api.student.schemas import Student
from src.api.student.service import StudentService
import src.api.student.dependencies as dependencies  


router = APIRouter(prefix="/students")


@router.post('/upload', status_code=status.HTTP_201_CREATED, response_model=list[Student])
async def upload_csv_file(file: UploadFile, hasher: Annotated[object, Depends(dependencies.get_hash)], db: Annotated[object, Depends(dependencies.get_db)] ):
    try:
        # Check if content-type is a text/csv
        if (file.content_type != 'text/csv'):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="CSV file must be provided")
        repository = StudentRepository(db)
        service = StudentService(repository)
        content = await file.read()
        content = content.decode("utf-8")

        res = service.create_students_from_string(content, hasher)
        
        return res
    except HTTPException as e:
        raise e