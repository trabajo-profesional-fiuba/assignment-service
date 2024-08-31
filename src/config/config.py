import os
from starlette.config import Config, environ
from starlette.datastructures import Secret


class ApiConfiguration:


    """
    The order in which configuration values are read is:

    - From an environment variable.
    - From the .env file.
    - The default value given in config.
    - If none of those match, then config(...) will raise an error.
    """

    def __init__(self) -> None:
        # Default to '.env.development' but use ENV_FILE if set
        config_file = os.getenv('ENV_FILE', '.env.development')
        print(f"Env file read: {config_file}")
        self.config = Config(config_file)

    @property
    def database_url(self) -> str:
        return self.config("DATABASE_URL", default="sqlite:///test.db")

    @property
    def database_pool_size(self) -> int:
        return self.config("DATABASE_POOL_SIZE", cast=int, default=10)

    @property
    def database_pool_timeout(self) -> int:
        return self.config("DATABASE_TIMEOUT", cast=int, default=10)

    @property
    def logging_level(self) -> str:
        return self.config("LOGGIN_LEVEL", default="INFO")

    @property
    def secret_key(self) -> Secret:
        return self.config("SECRET", cast=Secret, default="fake_secret")

    @property
    def hash_type(self) -> str:
        # HS256 (HMAC with SHA-256)
        return self.config("HASH", cast=str, default="HS256")

    @property
    def enviroment(self) -> str:
        return self.config("ENVIRONMENT", cast=str, default="DEV")

    @property
    def port(self) -> int:
        return self.config("PORT", cast=int, default=5000)

    @property
    def host(self) -> str:
        return self.config("HOST", cast=str, default="127.0.0.1")

    @property
    def api_version(self) -> str:
        return self.config("API_VERSION", cast=str, default="1.0.0")
    
    @property
    def workers(self) -> int:
        return self.config("WORKERS", cast=int, default=1)

    def set_env(self, key: str, value):
        environ[key.to_upper()] = value


api_config = ApiConfiguration()
