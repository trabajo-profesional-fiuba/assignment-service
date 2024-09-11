from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, Query, Response
from sqlalchemy.orm import Session

from src.api.assigments.service import AssigmentService
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.exceptions import EntityNotInserted, EntityNotFound, ServerError

from src.api.forms.repository import FormRepository
from src.api.forms.service import FormService
from src.api.groups.repository import GroupRepository
from src.api.groups.service import GroupService

from src.api.topics.repository import TopicRepository
from src.api.users.exceptions import InvalidCredentials

from src.config.database.database import get_db

router = APIRouter(prefix="/assigments", tags=["Assigments"])


@router.post(
    "/incomplete-groups",
    summary="Runs the assigment of incomplete groups",
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Successfully assigned groups"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unkown operation"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized to perform action"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happend inside the backend"
        },
    },
    status_code=status.HTTP_202_ACCEPTED,
)
async def assign_incomplete_groups(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period_id=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):  # tenemos que usarlo para recuperar los grupos de tal cuatrimestre
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        form_service = FormService(FormRepository(session))
        topic_repository = TopicRepository(session)
        group_service = GroupService(GroupRepository(session))

        answers = form_service.get_answers(topic_repository)
        service = AssigmentService()

        group_result = service.assigment_incomplete_groups(answers)
        group_service.create_basic_groups(group_result, period_id)
        return Response(status_code=status.HTTP_202_ACCEPTED, content="Created")
    except Exception as e:
        raise ServerError("error")
