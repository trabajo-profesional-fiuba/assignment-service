import datetime
import jwt as jwt_provider
from pydantic import BaseModel, Field

from src.config.config import api_config


class JwtEncoded(BaseModel):
    access_token: str
    type: str = Field(default="JWT")


class JwtDecoded(BaseModel):
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

    """ Gets timedelta of current time + minutes in utc(timedelta(0))"""

    def _get_exp_time(self, minutes):
        delta = datetime.timedelta(minutes=minutes)
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        time = now + delta
        return time.timestamp()

    """ Createas a 1hr token"""

    def create_token(self, sub, name, exp_time=None):
        if not exp_time:
            exp_time = self._get_exp_time(30)

        payload = {"sub": sub, "name": name, "exp": exp_time}
        token = jwt_provider.encode(
            payload=payload, key=str(self.secret), algorithm=self.hash
        )
        jwt = JwtEncoded(access_token=token, type="JWT")

        return jwt

    """ Attempts to decode the encoded jwt"""

    def decode_token(self, jwt: JwtEncoded):
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
