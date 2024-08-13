from typing_extensions import Annotated

from fastapi import APIRouter, UploadFile, Depends, status, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.api.users.repository import UserRepository
from src.api.tutors.service import TutorService
from src.api.tutors.schemas import (
    PeriodResponse,
    PeriodRequest,
    TutorResponse,
    TutorList,
    PeriodList,
)
from src.api.tutors.repository import TutorRepository
from src.api.tutors.exceptions import (
    InvalidTutorCsv,
    TutorDuplicated,
    PeriodDuplicated,
    TutorNotFound,
    InvalidPeriodId,
)
from src.api.auth.hasher import get_hasher, ShaHasher
from src.config.database.database import get_db

router = APIRouter(prefix="/tutors")


@router.post(
    "/upload",
    response_model=TutorList,
    description="Creates list of tutors based on a csv file",
    summary="Add csv file",
    tags=["Tutors"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "The columns are not correct"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated tutor"},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
            "description": "Content-Type is not correct."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
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
        service = TutorService(UserRepository(session))
        res = service.create_tutors_from_string(content, hasher)

        return res
    except InvalidTutorCsv as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message(),
        )
    except TutorDuplicated as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message(),
        )
    except HTTPException as e:
        raise e


@router.post(
    "/periods",
    response_model=PeriodResponse,
    description="Creates a new period",
    summary="Add a new period",
    tags=["Periods"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Period schema is not correct"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated period"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_period(
    session: Annotated[Session, Depends(get_db)], period: PeriodRequest
):
    try:
        service = TutorService(TutorRepository(session))
        return service.add_period(period)
    except PeriodDuplicated as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message(),
        )
    except InvalidPeriodId as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.message(),
        )
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/periods",
    response_model=PeriodList,
    description="Returns all the periods",
    summary="Get all periods",
    tags=["Periods"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_periods(
    session: Annotated[Session, Depends(get_db)],
    order: str = Query(pattern="^(ASC|DESC)$", default="DESC"),
):
    service = TutorService(TutorRepository(session))
    periods = service.get_all_periods(order)
    return periods


@router.post(
    "/{tutor_id}/periods",
    response_model=TutorResponse,
    description="Add new period for a tutor",
    summary="Add new period",
    tags=["Periods"],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Duplicated period"},
        status.HTTP_404_NOT_FOUND: {"description": "Tutor not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def add_period_to_tutor(
    session: Annotated[Session, Depends(get_db)],
    tutor_id: int,
    period_id: str = Query(...),
):
    try:
        service = TutorService(TutorRepository(session))
        return service.add_period_to_tutor(tutor_id, period_id)
    except PeriodDuplicated as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message(),
        )
    except TutorNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message(),
        )
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{tutor_id}/periods",
    response_model=TutorResponse,
    description="Returns all the periods for tutor_id",
    summary="Get all periods",
    tags=["Periods"],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Tutor not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def get_tutor_periods(
    session: Annotated[Session, Depends(get_db)],
    tutor_id: int,
):
    try:
        service = TutorService(TutorRepository(session))
        return service.get_periods_by_tutor_id(tutor_id)
    except TutorNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message(),
        )
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
