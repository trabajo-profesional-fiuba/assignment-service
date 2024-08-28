from src.api.auth.jwt import InvalidJwt, JwtResolver
from src.api.users.models import Role


class AuthenticationService:

    def __init__(self, jwt_resolver: JwtResolver) -> None:
        self._jwt_resolver = jwt_resolver

    def _assert_role(self, role, expected_role):
        if role != expected_role:
            raise InvalidJwt("Invalid jwt")

    def _assert_multiple_role(self, role, expected_roles):
        if role not in expected_roles:
            raise InvalidJwt("Invalid jwt")

    def assert_student_role(self, token: str):
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_multiple_role(user["role"], [Role.ADMIN.value, Role.STUDENT.value])

    def assert_only_admin(self, token: str):
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_role(user["role"], Role.ADMIN.value)

    def assert_tutor_rol(self, token: str):
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_multiple_role(user["role"], [Role.ADMIN.value, Role.TUTOR.value])
    
