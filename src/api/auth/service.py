from src.api.auth.jwt import InvalidJwt, JwtResolver
from src.api.auth.schemas import JwtDecoded
from src.api.users.models import Role


class AuthenticationService:
    def __init__(self, jwt_resolver: JwtResolver) -> None:
        self._jwt_resolver = jwt_resolver

    def _assert_role(self, role, expected_role):
        """Assert de un rol especifico"""
        if role != expected_role:
            raise InvalidJwt("Invalid jwt")

    def _assert_multiple_role(self, role, expected_roles):
        """Assert de multiples roles"""
        if role not in expected_roles:
            raise InvalidJwt("Invalid jwt")

    def assert_student_role(self, token: str) -> JwtDecoded:
        """Comprueba que el token sea un studiante o admin"""
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_multiple_role(user["role"], [Role.ADMIN.value, Role.STUDENT.value])
        return token_decoded

    def assert_only_admin(self, token: str) -> JwtDecoded:
        """Comprueba que el token sea un admin"""
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_role(user["role"], Role.ADMIN.value)
        return token_decoded

    def assert_tutor_rol(self, token: str, tutor_id: int | None = None) -> JwtDecoded:
        """
        Comprueba que el token sea un tutor o admin, en caso de tutor valida contra tutor_id si esta presente el arg
        """
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        if user["role"] == Role.TUTOR.value and tutor_id:
            if user["id"] != tutor_id:
                raise InvalidJwt("Invalid jwt")
        else:
            self._assert_multiple_role(
                user["role"], [Role.ADMIN.value, Role.TUTOR.value]
            )
        return token_decoded

    def assert_multiple_role(self, token: str) -> JwtDecoded:
        """Comprueba que sea o un estudiante, admin o tutor"""
        token_decoded = self._jwt_resolver.decode_token(token)
        user = token_decoded.sub
        self._assert_multiple_role(
            user["role"], [Role.ADMIN.value, Role.STUDENT.value, Role.TUTOR.value]
        )
        return token_decoded

    def get_user_id(self, token: str | JwtDecoded):
        """Obtiene el id del token"""
        if isinstance(token, str):
            token = self._jwt_resolver.decode_token(token)
        user = token.sub
        return user["id"]

    def is_admin(self, token: str | JwtDecoded) -> bool:
        """Indica si que el token pertenece a un admin"""
        try:
            if isinstance(token, str):
                token = self._jwt_resolver.decode_token(token)
            user = token.sub
            self._assert_role(user["role"], Role.ADMIN.value)
            return True
        except Exception:
            return False

    def is_student(self, token: str | JwtDecoded) -> bool:
        """Indica si que el token pertenece a un estudiante"""
        try:
            if isinstance(token, str):
                token = self._jwt_resolver.decode_token(token)
            user = token.sub
            self._assert_role(user["role"], Role.STUDENT.value)
            return True
        except Exception:
            return False

    def assert_student_in_group(self, token: str, group_id: str, group_repository):
        """Valida que un estudiante sea parte de un grupo"""
        jwt = self.assert_student_role(token=token)
        student_id = self.get_user_id(jwt)

        if not group_repository.student_in_group(student_id, group_id):
            raise InvalidJwt("Invalid jwt")
