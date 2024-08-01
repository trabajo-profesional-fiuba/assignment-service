from typing_extensions import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.auth.jwt import JwtResolver, JwtEncoded, get_jwt_resolver
from src.api.auth.hasher import ShaHasher, get_hasher
from src.config.database.database import get_db
from src.api.users.repository import UserRepository
from src.api.users.service import UserService
from src.api.users.exceptions import UserNotFound, InvalidCredentials


router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connect")


@router.post(
    "/connect",
    response_model=JwtEncoded,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "JWT token created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect username or password"},
    },
)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
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
            "rol": user.rol.value,
        }
        access_token = jwt_resolver.create_token(sub, user.name)
        return access_token
    except (UserNotFound, InvalidCredentials) as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))
