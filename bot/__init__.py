import json
import os

import discord
from discord.ext import commands

import env
import tasks
from consts import EXCLUDE_FILES
from utils import Log


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=">", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        if env.BOT_COGS != "ALL" and (
            not (env.BOT_COGS.startswith("[") and env.BOT_COGS.endswith("]"))
        ):
            Log.error("BOT", "Invalid format of env.BOT_COGS.")
            return

        cogs: list

        if env.BOT_COGS == "ALL":
            cogs = [
                "cogs." + command_file.removesuffix(".py")
                for command_file in os.listdir("cogs")
                if command_file.endswith(".py") and command_file not in EXCLUDE_FILES
            ]
        elif env.BOT_COGS.startswith("[") and env.BOT_COGS.endswith("]"):
            try:
                cogs = [
                    "cogs." + command_file.removesuffix(".py")
                    for command_file in os.listdir("cogs")
                    if command_file.endswith(".py")
                    and command_file not in EXCLUDE_FILES
                    and command_file.removeprefix("__").removesuffix("__.py")
                    in json.loads(env.BOT_COGS)
                ]
            except json.decoder.JSONDecodeError:
                Log.error("BOT", "Failed to parse env.BOT_COGS.")
                return

        for cog in cogs:
            await self.load_extension(cog)

        Log.info("BOT", f"{len(await self.tree.sync())} Slash Command(s).")

    async def on_ready(self):
        Log.info("BOT", f"Logged in as {self.user}")
        tasks.start(self)
