import env
import migration
from bot import Bot
from config import check_config
from utils import Log


def main():
    if env.IS_MISSING:
        return

    migration.run()

    if (missing_message := check_config()) is not None:
        Log.error("Bot", missing_message)
        return

    Bot().run(env.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
