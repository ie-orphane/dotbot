from .__challenges__ import *
from .__challenges__ import challenge as ChallengeConfig
from .__emojis__ import *
from .__self__ import *


def check_config() -> str | None:
    if get_config("GUILD") is None:
        return f"missing the GUILD field"
