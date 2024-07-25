import pytest
import datetime

from src.api.auth.jwt import JwtResolver, InvalidJwt


class TestJwtResolver:

    @pytest.mark.unit
    def test_jwt_resolver_can_creat_jwt(self):

        jwt_resolver = JwtResolver()
        sub = "1234567890"
        name = "Juan Perez"

        jwt = jwt_resolver.create_token(sub, name)
        jwt_as_dict = jwt.model_dump()

        assert "access_token" in jwt_as_dict
        assert "token_type" in jwt_as_dict

    @pytest.mark.unit
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


    @pytest.mark.unit
    def test_jwt_resolver_raise_invalid_jwt_if_it_is_expired(self):

        jwt_resolver = JwtResolver()
        sub = "1234567890"
        name = "Juan Perez"

        exp_time = datetime.datetime(2024,7,25,10).timestamp()
        jwt_expired = jwt_resolver.create_token(sub, name, exp_time)
        
        with pytest.raises(InvalidJwt) as e:
            _ = jwt_resolver.decode_token(jwt_expired)

