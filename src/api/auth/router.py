from typing_extensions import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends


from src.api.auth.jwt import JwtResolver, JwtEncoded, get_jwt_resolver
from src.api.auth.hasher import ShaHasher, get_hasher
from src.api.auth.schemas import RequestForm

from src.config.database.database import get_db
from src.api.users.repository import UserRepository
from src.api.users.service import UserService
from src.api.users.exceptions import UserNotFound, InvalidCredentials


router = APIRouter(tags=["Authentication"])



@router.post(
    "/connect",
    response_model=JwtEncoded,
    summary="Authenticate User and Generate JWT Token",
    description="""This endpoint is used for user authentication.
    By submitting valid credentials (such as a username and password) in the
    request body, you can obtain a JWT (JSON Web Token) for accessing protected
    resources.
    If the credentials are correct, a JWT token will be issued and returned in
    the response.
    If the credentials are incorrect, an error response will be generated.
    This token should be used in subsequent requests to access secure endpoints.""",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "JWT token successfully created. The response contains the\
            token details."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication failed. The username or password provided is\
            incorrect. Ensure credentials are correct and try again."
        },
    },
)
async def get_access_token(
    form_data: Annotated[RequestForm, Depends()],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
) -> JwtEncoded:

    try:
        email = form_data.username
        hashed_password = hasher.hash(form_data.password)

        repository = UserRepository(session)
        service = UserService(repository)
        user = service.authenticate(email, hashed_password)
        sub = {
            "id": user.id,
            "name": user.name,
            "last_name": user.last_name,
            "role": user.role.value,
        }
        access_token = jwt_resolver.create_token(sub, user.name)
        return access_token
    except (UserNotFound, InvalidCredentials) as e:
        raise e
