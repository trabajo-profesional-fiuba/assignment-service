from datetime import datetime
from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.api.forms.schemas import (
    FormPreferencesRequest,
    FormPreferencesList,
    FormPreferencesResponse,
    GroupAnswerList,
    GroupAnswerResponse,
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
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db
from src.config.logging import logger

router = APIRouter(prefix="/forms", tags=["Forms"])


@router.post(
    "/answers",
    description="This endpoint creates answers for sender and group members",
    response_model=FormPreferencesList,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Successfully added topic preferences answers."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a \
            client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_answers(
    answers: FormPreferencesRequest,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Agrega una nueva respuesta del formulario de armado de grupos y seleccion de temas"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        service = FormService(FormRepository(session))
        answers_saved = service.add_answers(answers, period)

        res = FormPreferencesList.model_validate(
            [
                FormPreferencesResponse(
                    user_id=answer.id,
                    answer_id=answer.answer_id,
                    topic_1=answer.topics[0],
                    topic_2=answer.topics[1],
                    topic_3=answer.topics[2],
                )
                for answer in answers_saved
            ]
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (Duplicated, EntityNotFound) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/answers",
    summary="This endpoint return all answers grouped by answer id.",
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
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Obtiene todas las respuestas del formulario de armado de grupos y seleccion de temas"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        service = FormService(FormRepository(session))
        answers = service.get_answers(TopicRepository(session), period)
        response = list()
        for answer in answers:
            response.append(
                GroupAnswerResponse(
                    id=answer.id,
                    students=answer.students,
                    topics=answer.get_topic_names(),
                )
            )
        res = GroupAnswerList.model_validate(response)

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        logger.error("Could not get all the answers from the db")
        raise ServerError(message=str(e))


@router.get(
    "/answers/{user_id}",
    summary="This endpoint return all topic preferences answers of a user by id",
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
async def get_answers_by_user_id(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    user_id: int,
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    """Obtiene todas las respuestas de un alumno"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)
        service = FormService(FormRepository(session))
        res = service.get_answers_by_user_id(user_id, TopicRepository(session), period)

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        logger.error("Could not get all the answers from the db")
        raise ServerError(message=str(e))


@router.delete(
    "/answers/{answer_id}",
    summary="This endpoint deletes answers by answer id.",
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
    """Borra una respuesta por id"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = FormService(FormRepository(session))
        res = service.delete_answers_by_answer_id(answer_id)

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_200_OK)
    except EntityNotFound as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
