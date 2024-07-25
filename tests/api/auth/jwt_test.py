import pytest
import datetime

from src.api.auth.jwt import JwtResolver


class TestJwtResolver:

    def test_jwt_resolver_can_creat_jwt(self):

        jwt_resolver = JwtResolver()
        sub = "1234567890"
        name = "Juan Perez"

        jwt = jwt_resolver.create_token(sub, name)
        jwt_as_dict = jwt.model_dump()

        assert "access_token" in jwt_as_dict
        assert "type" in jwt_as_dict


    def test_jwt_resolver_can_decode_jwt(self):

        jwt_resolver = JwtResolver()
        sub = "1234567890"
        name = "Juan Perez"

        jwt = jwt_resolver.create_token(sub, name)
        decoded_jwt = jwt_resolver.decode_token(jwt)
        jwt_info = dict(decoded_jwt)

        assert "sub" in jwt_info
        assert "name" in jwt_info
        assert "exp" in jwt_info
