from datetime import datetime
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from src.api.forms.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    GroupAnswerList,
    UserAnswerList,
)
from src.api.forms.repository import FormRepository
from src.api.forms.service import FormService
from src.api.topics.repository import TopicRepository

from src.api.exceptions import (
    EntityNotFound,
    Duplicated,
    ServerError,
)
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.users.exceptions import InvalidCredentials
from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/forms", tags=["Forms"])


@router.post(
    "/answers",
    description="This endpoint creates topic preferences answers for sender\
        and students from its group if it belongs to one.",
    response_model=FormPreferencesList,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successfully added topic preferences answers."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happend inside the backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_answers(
    answers: FormPreferencesRequest,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)
        service = FormService(FormRepository(session))
        return service.add_answers(answers)
    except (Duplicated, EntityNotFound) as e:
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/answers",
    description="This endpoint return all topic preferences answers grouped by answer \
        id.",
    response_model=GroupAnswerList,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully get all answers grouped by answer id."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_answers(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = FormService(FormRepository(session))
        return service.get_answers(TopicRepository(session), for_controller=True)
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        logger.error("Could not get all the answers from the db")
        raise ServerError(message=str(e))


@router.get(
    "/answers/{user_id}",
    description="This endpoint return all topic preferences answers of a user by id",
    response_model=UserAnswerList,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully get all answers grouped by answer id."
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_answers(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    user_id: int,
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)
        service = FormService(FormRepository(session))
        return service.get_answers_by_user_id(user_id, TopicRepository(session))
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        logger.error("Could not get all the answers from the db")
        raise ServerError(message=str(e))


@router.delete(
    "/answers/{answer_id}",
    description="This endpoint deletes answers by answer id.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully deleted answers by answer id."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_answer(
    answer_id: datetime,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = FormService(FormRepository(session))
        return service.delete_answers_by_answer_id(answer_id)
    except EntityNotFound as e:
        raise e
    except InvalidJwt as e:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
