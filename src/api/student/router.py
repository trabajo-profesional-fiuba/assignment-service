from fastapi import APIRouter, UploadFile
from fastapi.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException


from src.api.student.schemas import StudentResponse
from src.api.student.service import StudentService


router = APIRouter(prefix="/students")


@router.post('/upload', status_code=status.HTTP_201_CREATED, response_model=list[StudentResponse])
async def upload_csv_file(file: UploadFile):
    try:
        # Check if content-type is a text/csv
        if (file.content_type != 'text/csv'):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="CSV file must be provided")
        
        service = StudentService(None)
        content = await file.read()
        content = content.decode("utf-8")

        res = service.create_students_from_string(content)
        
        return res
    except Exception as e:
        # Re-raise the HTTPException to let FastAPI handle it
        raise e