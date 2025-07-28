import json

import env
from config import ChallengeConfig, get_challenge_by_id

from .__self__ import Document
from .__users__ import User, solution

__all__ = ["Evaluation"]


class Evaluation(Document):
    BASE: str = "evaluations"
    solution: solution
    user: User
    challenge: ChallengeConfig
    timestamp: str

    def __to_dict__(self):
        self.__dict__.update(
            user=self.user.id,
            id=self.challenge.id,
        )
        self.__dict__.pop("challenge", None)
        return self.__dict__

    @classmethod
    def read_all(cls):
        with open(f"{env.BASE_DIR}/data/{cls.BASE}.json") as file:
            return [
                cls(
                    timestamp=x["timestamp"],
                    user=User.read(x["user"]),
                    challenge=get_challenge_by_id(x["id"]),
                )
                for x in json.load(file)
            ]

    @property
    def solution(self):
        return solution(filename=f"{self.timestamp}.{self.challenge.extension}")

    def log(self, *content: str, sep="\n", end="\n"):
        with open(
            f"{env.BASE_DIR}/storage/evaluations/{self.timestamp}.ansi.log",
            "a",
        ) as f:
            f.write(sep.join(content) + end)
