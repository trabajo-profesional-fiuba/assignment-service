import datetime
import jwt as jwt_provider
from src.api.auth.schemas import JwtDecoded, JwtEncoded
from src.config.config import api_config
from src.config.logging import logger


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
        Obtiene el intervalo de tiempo de la hora actual + minutos en UTC (timedelta(0)).
        El Tiempo Universal Coordinado (UTC) es el estándar de tiempo principal utilizado globalmente para regular relojes y el tiempo.
        Establece una referencia para la hora actual, formando la base para el tiempo civil y las zonas horarias
        """
        delta = datetime.timedelta(minutes=minutes)
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        time = now + delta
        return time.timestamp()

    def create_token(self, sub, name, exp_time=None) -> JwtEncoded:
        """
        Crea un nuevo JWT con las reclamaciones 'sub', 'name' y 'exp', donde si exp_time es None, establece un JWT de 30 minutos.
        """
        if not exp_time:
            exp_time = self._get_exp_time(30)

        payload = {"sub": sub, "name": name, "exp": exp_time}
        token = jwt_provider.encode(
            payload=payload, key=str(self.secret), algorithm=self.hash
        )
        jwt = JwtEncoded(access_token=token, token_type="Bearer")
        logger.info(f"New JWT created for {name} at {exp_time}")
        return jwt

    def decode_token(self, jwt: str) -> JwtDecoded:
        """
        Decodifica el jwt
        """
        try:
            jwt_decoded = jwt_provider.decode(
                jwt,
                str(self.secret),
                algorithms=[self.hash],
                options={"verify_exp": self.verify_exp},
            )

            return JwtDecoded(**jwt_decoded)
        except Exception as e:
            logger.error("Invalid Jwt")
            raise InvalidJwt(message=str(e))


# TODO - Moverlo a un archivo .py
def get_jwt_resolver():
    yield JwtResolver()
