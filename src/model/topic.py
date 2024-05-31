class Topic:
    """
    Class representing a topic.

    Attributes:
        id (str): The identifier of the topic.
    """

    def __init__(self, id: str) -> None:
        """
        Initializes a Topic object with the given ID.

        Args:
            id (str): The identifier of the topic.
        """
        self._id = id

    @property
    def id(self) -> str:
        """
        Get the identifier of the topic.

        Returns:
            str: The identifier of the topic.
        """
        return self._id
