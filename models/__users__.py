from datetime import UTC, datetime
from typing import Self

import env
from config import (
    ChallengeConfig,
    get_challenge_by_id,
    get_challenge_by_level,
    get_challenges,
)
from notations import CHALLENGE

from .__self__ import Collection, Model

__all__ = [
    "User",
    "UserChallenge",
]


class Log(Model):
    name: str
    id: int
    attempt: int
    trace: str
    result: CHALLENGE.RESULT
    cost: int


class filebase(Model):
    BASE: str
    filename: str

    def __init_subclass__(cls, BASE=None):
        if BASE is None:
            raise ValueError("BASE must be defined in the subclass")
        if not isinstance(BASE, str):
            raise TypeError("BASE must be a string")
        if not BASE:
            raise ValueError("BASE cannot be empty")
        cls.BASE = BASE

    @property
    def path(self):
        return f"{env.BASE_DIR}/storage/{self.BASE}/{self.filename}"


class solution(filebase, BASE="solutions"): ...


class UserChallenge(ChallengeConfig):
    attempt: int
    requested: datetime
    submited: datetime = None
    evaluated: datetime = None
    result: CHALLENGE.RESULT = None
    log: str = None
    timestamp: str = None

    def __init__(self, id: str, **kwargs) -> None:
        self.__dict__.update({**kwargs, **get_challenge_by_id(id).__dict__})

    @property
    def solution(self) -> solution:
        if self.timestamp is None:
            self.timestamp = str(datetime.now(UTC).timestamp()).replace(".", "_")
        return solution(filename=f"{self.timestamp}.{self.extension}")


class User(Collection):
    BASE = "users"
    id: int
    name: str
    _challenges: list[dict]
    _challenge: dict | None = None
    _log: dict | None = None
    cooldowns: dict | None = None

    @property
    def challenge(self):
        if self._challenge:
            return UserChallenge(**self._challenge)
        return None

    @property
    def log(self):
        if self._log:
            return Log(**self._log)
        return None

    @property
    def challenges(self):
        return [UserChallenge(**challenge_data) for challenge_data in self._challenges]

    @property
    def mention(self):
        return f"<@{self.id}>"

    @classmethod
    def read(cls, id: int) -> Self | None:
        return super().read(id)

    @classmethod
    def create(cls, id: int, name: str) -> Self:
        user = cls(id=id, name=name, _challenges=[])
        user.update()
        return user

    def request(self):
        if (all_challenges := get_challenges()) is None:
            return None

        user_challenges = self.challenges

        all_user_challenges: dict[tuple[int, str], list[UserChallenge]] = {}

        for challenge in user_challenges:
            all_user_challenges.setdefault((challenge.level, challenge.name), [])
            all_user_challenges[(challenge.level, challenge.name)].append(challenge)

        all_user_challenges = dict(
            sorted(all_user_challenges.items(), key=lambda x: x[0][0])
        )

        level = 0
        attempt = 1
        for challenges in all_user_challenges.values():
            challenges.sort(key=lambda x: x.attempt)
            for challenge in challenges:
                if level == challenge.level:
                    if challenge.result == "OK":
                        level += 1
                        attempt = 1
                    else:
                        attempt += 1

        if level >= len(all_challenges):
            return None

        challenge = get_challenge_by_level(level)

        self._challenge = {
            "id": challenge.id,
            "attempt": attempt,
            "requested": str(datetime.now(UTC)),
        }

        self.update()

        return challenge
