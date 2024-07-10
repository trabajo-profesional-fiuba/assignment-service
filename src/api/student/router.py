from fastapi import APIRouter
from fastapi.requests import Request
from fastapi import status

from src.api.student.schemas import StudentResponse


router = APIRouter(prefix="/students")


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[StudentResponse])
async def get_all_students():

    return []
