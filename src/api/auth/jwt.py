import datetime
import jwt as jwt_provider
from pydantic import BaseModel, Field

from src.config.config import api_config


class JwtEncoded(BaseModel):
    """Schema to represent a Jwt encoded"""

    # TODO - Refresh token if necessary.
    access_token: str
    token_type: str = Field(default="JWT")


class JwtDecoded(BaseModel):
    """Schema to represent a Jwt with its claims decoded"""

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
        """Gets timedelta of current time + minutes in utc(timedelta(0))"""
        delta = datetime.timedelta(minutes=minutes)
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        time = now + delta
        return time.timestamp()

    """ Createas a 1hr token"""

    def create_token(self, sub, name, exp_time=None) -> JwtEncoded:
        """Creates a new Jwt with the claims 'sub', 'name','exp'
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
