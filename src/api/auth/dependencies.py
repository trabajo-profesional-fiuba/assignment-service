from typing import Annotated

from fastapi import Depends

from src.api.auth.jwt import JwtResolver
from src.api.auth.schemas import oauth2_scheme


def get_jwt_resolver():
    return JwtResolver()


def authorization(
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
):
    # Maneja la autorización obteniendo el token y resolviendo el JWT para validarlo.
    # Mas info de subdependencies en
    # https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/
    return {"token": token, "jwt_resolver": jwt_resolver}
