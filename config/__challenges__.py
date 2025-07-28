import random
import re
import string
from typing import Literal

import env
from notations import CHALLENGE

from .__self__ import config, get_config

__all__ = [
    "get_challenges",
    "get_challenge_by_level",
    "get_challenge_by_id",
    "get_challenge_by_name",
]


class _test(config):
    description: str
    args: list[str]
    expected: str
    input: str | None = None
    _args: list[str] = []
    _expected: str
    _input: str = None
    __parsed: dict[str, str]

    @staticmethod
    def __range(match: re.Match[str]) -> str:
        """
        Expand charset patterns like 'a-zA-Z0-9' using regex to find ranges.

        Example
        --------
        >>> x-zA-Z
        'xyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        Args
        -----
            match (Match[str]): The regex match object.

        Returns
        --------
            str: The expanded string.
        """
        start, end = match.groups()
        return "".join(chr(c) for c in range(ord(start), ord(end) + 1))

    def __str(self, match: re.Match[str]) -> str:
        """
        Generate a random string of a given length. `{name:str:length}`

        Example
        --------
        >>> {word:str:10}
        'aBcD1234Ef'

        Args
        -----
            match (Match[str]): The regex match object.

        Returns
        --------
            str: The generated random string.
        """
        name, length, charset = match.groups()
        charset = (
            string.ascii_letters + string.digits
            if charset is None
            else re.sub(r"([A-Za-z0-9])-([A-Za-z0-9])", self.__range, charset)
        )
        randarg = "".join(random.choices(charset, k=int(length)))
        if name is not None:
            self.__parsed[name] = randarg
        return randarg

    def __int(self, match: re.Match[str]) -> str:
        """
        Generate a random integer between two values. `{name:int:min:max}`

        Example
        --------
        >>> {number:int:1:10}
        5

        Args
        -----
            match (Match[str]): The regex match object.

        Returns
        --------
            str: The generated random integer.
        """
        name, _min, _max = match.groups()
        randarg = random.randint(int(_min), int(_max))
        if name is not None:
            self.__parsed[name] = randarg
        return str(randarg)

    def __expr(self, match: re.Match[str]) -> str:
        """
        Evaluate an expression. `$<name>expression<$`

        Example
        --------
        >>> $<result>1 + 2 * 3<$
        7

        Args
        -----
            match (Match[str]): The regex match object.

        Returns
        --------
            str: The result of the evaluated expression.
        """
        name, expression = match.groups()
        result = str(eval(expression))
        if name is not None:
            self.__parsed[name] = result
        return result

    def __parse(self, string: str) -> str:
        """
        Parse the given string and replace the placeholders with the corresponding values.

        Args
        -----
            string (str): The string to parse.

        Returns
        --------
            str: The parsed string.
        """
        if not isinstance(string, str):
            raise TypeError(f"Expected str, got {type(string)}")
        string = re.sub(r"\{(?:(\w+):)?int:(-?\d+):(-?\d+)\}", self.__int, string)
        string = re.sub(r"\{(?:(\w+):)?str:(\d+)(?::([^}]+))?\}", self.__str, string)
        string = re.sub(r"\$\<?(\w+)?\>(.*)\<\$", self.__expr, string)
        return string

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__parsed = dict()
        self.args = [self.__parse(arg) for arg in self._args]
        if self._input is not None:
            self.input = self.__parse(self._input)
        self.expected = self.__parse(self._expected.format(**self.__parsed))


class challenge(config):
    """challenge config class.
    Attributes:
        id (`str`): The ID of the challenge.
        forbidden (`list`): List of forbidden commands/functions/libraries.
        extension (`str`): The file extension for the challenge.
        runner (`str`): The runner for the challenge.
        name (`str`): The name of the challenge.
        level (`str`): The level of the challenge.
        _tests (`list`): The tests for the challenge.
        difficulty (`str`): The difficulty level of the challenge.
        additionales (`str`): Additional code for the challenge.
        not_allowed (`list`): List of not allowed commands/functions/libraries.
        file (`str`): The filename of the challenge.
        tests (`list`[`test`]): The tests for the challenge.
        subject (`str`): The subject of the challenge.
    """

    runner: Literal["python3", "python"]
    extension: Literal["py"] = "py"

    id: str
    name: str
    level: str
    _tests: list[dict]
    difficulty: CHALLENGE.DIFFICULTY
    additionales: str = ""
    not_allowed: list[str] = []

    @property
    def file(self) -> str:
        return f"{self.name}.{self.extension}"

    @property
    def tests(self) -> list[_test]:
        return [_test(**test) for test in self._tests]

    @property
    def subject(self) -> str:
        with open(f"{env.BASE_DIR}/storage/subjects/{self.id}.ansi") as file:
            return file.read()


def get_challenges() -> list[challenge]:
    """
    Get all challenges.
    Returns:
        `list`[`challenge`]: A list of challenges.
    """
    if (challenges := get_config("CHALLENGES")) is None:
        return None
    if not isinstance(challenges, list):
        raise TypeError("Expected a list of challenges.")
    return [
        challenge(**_challenge, level=level, runner=get_config("RUNNER") or "python3")
        for level, _challenge in enumerate(challenges)
    ]


def get_challenge_by_level(level: int) -> challenge | None:
    r"""
    Get a challenge for a given level.
    Args:
        level (`int`): The level of the challenge to get.
    Returns:
        `challenge` | `None`: The challenge for the given level, or None if not found.
    """
    challenges = get_challenges()
    if challenges is None or level < 0 or level >= len(challenges):
        return None
    return challenges[level]


def get_challenge_by_id(id: str) -> challenge | None:
    r"""
    Get a challenge for a given id.
    Args:
        id (`str`): The ID of the challenge to get.
    Returns:
        `challenge` | `None`: The challenge for the given id, or None if not found.
    """
    challenges = get_challenges()
    if challenges is None:
        return None
    for challenge in challenges:
        if challenge.id == id:
            return challenge
    return None


def get_challenge_by_name(name: str) -> challenge | None:
    r"""
    Get a challenge for a given name.
    Args:
        name: `str`: The name of the challenge to get.
    Returns:
        `challenge` | `None`: The challenge for the given name, or None if not found.
    """
    challenges = get_challenges()
    if challenges is None:
        return None
    for challenge in challenges:
        if challenge.name == name:
            return challenge
    return None
