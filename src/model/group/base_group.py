class BaseGroup:
    """
    A base class representing a group.
    """

    def __init__(self, id: str) -> None:
        """
        Initializes a BaseGroup object with the provided identifier.

        Params:
            - id (str): The identifier of the group.
        """
        self._id: str = id

    @property
    def id(self) -> str:
        """
        Retrieves the identifier of the group.

        Returns:
            str: The identifier of the group.
        """
        return self._id
