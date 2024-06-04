from src.model.group.group import Group


class AssignmentResult:

    def __init__(
        self,
        groups: list[Group],
    ) -> None:
        self._groups: groups
