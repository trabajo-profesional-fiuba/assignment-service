from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="connect")


class RequestForm(OAuth2PasswordRequestForm):
    pass


class JwtEncoded(BaseModel):
    """
    Schema to represent a Jwt encoded,
    the fields that this jwt contains are the actual token as
    the access token and the token type which is now Jwt

    More information at https://jwt.io/
    """

    access_token: str
    token_type: str = Field(default="Bearer")


class JwtDecoded(BaseModel):
    """
    Schema to represent a Jwt when it is decoded.
    Som claims are considerer obligatory to have
    such as:

    sub - It is the subject of the Json Web Token
    name - The name of the jwt's owner
    exp - Expired date as a timestamp
    """

    sub: dict
    name: str
    exp: float


class Token(BaseModel):
    token: str
