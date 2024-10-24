from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.api.admins.schemas import AdminRequest
from src.api.admins.service import AdminService
from src.api.auth.hasher import get_hasher, ShaHasher
from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.exceptions import Duplicated, ServerError
from src.api.users.exceptions import InvalidCredentials
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserResponse
from src.api.utils.response_builder import ResponseBuilder
from src.config.database.database import get_db

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.post(
    "",
    response_model=UserResponse,
    summary="Add a new admin",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Admin schema is not correct"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_409_CONFLICT: {"description": "Duplicated admin"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_admin(
    admin: AdminRequest,
    hasher: Annotated[ShaHasher, Depends(get_hasher)],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    """Endpoint para crear un nuevo administrador siendo administrador"""
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)
        service = AdminService(UserRepository(session))

        res = UserResponse.model_validate(service.add_admin(hasher, admin))

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except Duplicated as e:
        raise Duplicated("Duplicated admin")
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(str(e))
