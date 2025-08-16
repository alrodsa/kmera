from enum import Enum

class NamingMode(Enum):
    """
    Enum to represent the different modes of operation.
    """
    COPY = "copy"
    REPLACE = "replace"

    def __str__(self) -> str:
        """
        Returns the string representation of the mode.
        """
        return self.value

    @classmethod
    def choices(cls) -> list[str]:
        """
        Returns a list of available modes.
        """
        return [mode.value for mode in cls]
