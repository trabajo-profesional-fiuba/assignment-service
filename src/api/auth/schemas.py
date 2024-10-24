from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connect")


class RequestForm(OAuth2PasswordRequestForm):
    """Encapsula OAuth2PasswordRequestForm en una clase interna"""

    ...


class JwtEncoded(BaseModel):
    """
    Esquema para representar un JWT codificado
    Los campos que este JWT contiene son el token actual como el token de acceso y el tipo de token que ahora es JWT.

    Más información en https://jwt.io/
    """

    access_token: str
    token_type: str = Field(default="Bearer")


class JwtDecoded(BaseModel):
    """
    Esquema para representar un JWT cuando está decodificado. 
    Algunas reclamaciones se consideran obligatorias, tales como:

    - sub: Es el sujeto del Json Web Token.
    - name: El nombre del propietario del JWT.
    - exp: Fecha de expiración como una marca de tiempo.
    """

    sub: dict
    name: str
    exp: float


class PasswordResetRequest(BaseModel):
    old_password: str
    new_password: str
