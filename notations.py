from typing import Literal


class CHALLENGE:
    """
    Definitions of the notations used in the challenge.
    Attributes:
        EXTENSION (Literal): The file extension of the challenge.
        DIFFICULTY (Literal): The difficulty level of the challenge.
        RESULT (Literal): The result of the challenge.
        RUNNER (Literal): The runner for the challenge.
    """

    """DIFFICULTY: The difficulty level of the challenge."""
    DIFFICULTY = Literal["easy", "medium", "hard"]
    """RESULT: The result of the challenge."""
    RESULT = Literal["OK", "KO", "ERROR", "TIMEOUT", "DEAD", "FORBIDDEN"]
