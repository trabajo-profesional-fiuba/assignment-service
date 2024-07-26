from typing_extensions import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.auth.jwt import JwtResolver, JwtEncoded, get_jwt_resolver
from src.api.auth.hasher import ShaHasher, get_hasher
from src.config.database import get_db

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connect")


@router.post(
    "/connect",
    response_model=JwtEncoded,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "JWT token created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect username or password"}
    },
)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)]

) -> JwtEncoded:
    
    user =  form_data.username
    password = form_data.password

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = jwt_resolver.create_token("subject!", user)
    return access_token
