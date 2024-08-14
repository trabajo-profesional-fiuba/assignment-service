import datetime
import jwt as jwt_provider
from pydantic import BaseModel, Field

from src.config.config import api_config
from src.config.logging import logger


class JwtEncoded(BaseModel):
    """
    Schema to represent a Jwt encoded,
    the fields that this jwt contains are the actual token as
    the access token and the token type which is now Jwt

    More information at https://jwt.io/
    """

    access_token: str
    token_type: str = Field(default="Jwt Bearer token")


class JwtDecoded(BaseModel):
    """
    Schema to represent a Jwt when it is decoded.
    Som claims are considerer obligatory to have
    such as:

    sub - It is the subject of the Json Web Token
    name - The name of the jwt's owner
    exp - Expired date as a timestamp
    """

    sub: str
    name: str
    exp: float


class InvalidJwt(Exception):

    def __init__(self, message) -> None:
        super().__init__()
        self._message = message

    @property
    def message(self):
        return self._message


class JwtResolver:

    def __init__(self, verify_exp: bool = True) -> None:
        self.secret = api_config.secret_key
        self.verify_exp = verify_exp
        self.hash = api_config.hash_type

    def _get_exp_time(self, minutes) -> float:
        """
        Gets timedelta of current time + minutes in utc(timedelta(0)).
        Coordinated Universal Time (UTC) is the primary time standard globally used to regulate clocks and time.
        It establishes a reference for the current time, forming the basis for civil time and time zones.
        """
        delta = datetime.timedelta(minutes=minutes)
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        time = now + delta
        return time.timestamp()

    def create_token(self, sub, name, exp_time=None) -> JwtEncoded:
        """
        Creates a new Jwt with the claims 'sub', 'name','exp'
        where if the exp_time is none, it sets a 30min jwt.
        """
        if not exp_time:
            exp_time = self._get_exp_time(30)

        payload = {"sub": sub, "name": name, "exp": exp_time}
        token = jwt_provider.encode(
            payload=payload, key=str(self.secret), algorithm=self.hash
        )
        jwt = JwtEncoded(access_token=token, token_type="JWT")

        return jwt

    def decode_token(self, jwt: JwtEncoded) -> JwtDecoded:
        """Attempts to decode the encoded jwt
        with the expire verification based on the
        attr set.
        """
        try:
            jwt_decoded = jwt_provider.decode(
                jwt.access_token,
                str(self.secret),
                algorithms=[self.hash],
                options={"verify_exp": self.verify_exp},
            )

            return JwtDecoded(**jwt_decoded)
        except Exception as e:
            raise InvalidJwt(message=str(e))


def get_jwt_resolver():
    yield JwtResolver()
