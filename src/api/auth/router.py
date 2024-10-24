from fastapi import APIRouter, BackgroundTasks, Response, status, Depends
from sqlalchemy.orm import Session

from src.api.auth.hasher import ShaHasher, get_hasher
from src.api.auth.jwt import JwtResolver, JwtEncoded, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.schemas import PasswordResetRequest, RequestForm
from src.api.auth.service import AuthenticationService
from src.api.groups.dependencies import get_email_sender
from typing_extensions import Annotated
from src.api.users.exceptions import (
    InvalidPasswordReset,
    UserNotFound,
    InvalidCredentials,
)
from src.api.users.repository import UserRepository
from src.api.users.service import UserService
from src.config.database.database import get_db

router = APIRouter(tags=["Authentication"])

@router.post(
    "/connect",
    response_model=JwtEncoded,
    summary="Authenticate User and Generate JWT Token",
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
    """ Autentica el usuario y crea un token JWT de acceso"""
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


@router.post(
    "/reset-password",
    summary="Authenticate User and Generate JWT Token",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Password reset."},
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication failed. The username or password provided is\
            incorrect. Ensure credentials are correct and try again."
        },
    },
)
async def reset_password(
    password_request: PasswordResetRequest,
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    email_sender: Annotated[object, Depends(get_email_sender)],
    background_tasks: BackgroundTasks,
) -> JwtEncoded:
    """ Endpoint para resetear la contraseña del usuario enviando un mail como tarea en async"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        jwt = auth_service.assert_multiple_role(token)
        user_id = auth_service.get_user_id(jwt)

        old_password = hasher.hash(password_request.old_password)
        new_password = hasher.hash(password_request.new_password)

        service = UserService(UserRepository(session))
        user = service.update_user_password(user_id, old_password, new_password)

        to = user.email
        subject = "Tu contraseña fue actualizada con éxito"
        msg = f"""
        Hola {user.name}, queríamos comunicarte que tu contraseña ha sido modificada con éxito.\n
        El responsable de esta cuenta es: {user.email}
        Tu nueva contraseña es: {password_request.new_password}\n
        Agrega este mail a favoritos.
        Si no fuiste vos, comunicate inmediatamente con algún integrante del equipo: avillores@fi.uba.ar, vlopez@fi.uba.ar, ipfaab@fi.uba.ar, cdituro@fi.uba.ar
        """

        background_tasks.add_task(
            email_sender.send_email, to=to, subject=subject, body=msg
        )
        return Response(status_code=status.HTTP_202_ACCEPTED)
    except (UserNotFound, InvalidCredentials, InvalidPasswordReset) as e:
        raise e
