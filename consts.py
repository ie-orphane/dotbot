import math

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2


EXCLUDE_DIRS = ["__pycache__", ".git", ".venv", "venv"]


# ------ config ------
class Config:
    DIR: str = "bot"
    SUFFIX: str = "config.json"

    @property
    def path(self):
        return f"{self.DIR}/{self.FILE}"

    @classmethod
    def path(cls, field: str):
        return f"{cls.DIR}/{field}.{cls.SUFFIX}"


# Exclude files that should not be imported
EXCLUDE_FILES = ["__init__.py", "__all__.py", "__self__.py"]
