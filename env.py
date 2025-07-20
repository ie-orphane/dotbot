"""
load and store enviroment variables from the .env

### Raises:
- `AttributeError`: if env variable not found
"""

import os
from dotenv import load_dotenv

from utils.__log__ import Log

load_dotenv()

IS_MISSING: bool = False

DISCORD_BOT_TOKEN: str

BOT_TASKS: str
BOT_COGS: str

BASE_DIR: str


for env_variable_name in __annotations__:
    if globals().get(env_variable_name) is not None:
        continue

    if ((env_variable := os.environ.get(env_variable_name)) is None) or (env_variable == ""):
        Log.error("ENV", f"missing {env_variable_name}")
        IS_MISSING = True
        exit(1)


    exec(f"{env_variable_name} = '{env_variable}'")

