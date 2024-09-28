from fastapi import APIRouter, status, Depends, UploadFile, Query
from typing_extensions import Annotated
from sqlalchemy.orm import Session


from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService

from src.api.exceptions import EntityNotFound, InvalidCsv, InvalidFileType, ServerError

from src.api.topics.repository import TopicRepository
from src.api.topics.schemas import TopicList
from src.api.topics.service import TopicService

from src.api.tutors.repository import TutorRepository

from src.api.users.exceptions import InvalidCredentials

from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db


router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post(
    "/upload",
    response_model=TopicList,
    description="Creates a list of topics based on a csv file.",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added topics."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Columns don't match with expected."
        },
        status.HTTP_409_CONFLICT: {"description": "Topic already exists."},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Invalid file type."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error."
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def upload_csv_file(
    file: UploadFile,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period: str = Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        if file.content_type != "text/csv":
            raise InvalidFileType("CSV file must be provided.")
        content = (await file.read()).decode("utf-8")
        service = TopicService(TopicRepository(session))

        res = service.create_topics_from_string(
            period, content, TutorRepository(session)
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (
        EntityNotFound,
        InvalidFileType,
        InvalidCsv,
    ) as e:
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))


@router.get(
    "/",
    response_model=TopicList,
    description="Get a list of topics.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error."
        },
    },
)
async def get_topics(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        service = TopicService(TopicRepository(session))
        topics = service.get_topics()

        return ResponseBuilder.build_private_cache_response(topics)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))
