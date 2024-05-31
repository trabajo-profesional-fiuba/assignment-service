class BaseTutor:
    """
    A base class representing a tutor.
    """

    def __init__(self, id: str) -> None:
        """
        Initializes a BaseTutor object with the provided identifier.

        Params:
            - id (str): The identifier of the tutor.
        """
        self._id: str = id

    @property
    def id(self) -> str:
        """
        Retrieves the identifier of the tutor.

        Returns:
            str: The identifier of the tutor.
        """
        return self._id
