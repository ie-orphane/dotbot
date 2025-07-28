import discord

from cogs import Cog
from models import UserChallenge
from utils import RelativeDateTime


class Status(Cog):
    @discord.app_commands.dm_only()
    @discord.app_commands.allowed_installs(guilds=False, users=True)
    @discord.app_commands.command(description="See the history of your journey.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.cog_interaction(interaction)

        if (user := await self.bot.user_is_unkown(interaction)) is None:
            return

        all_challenges: dict[tuple[int, str], list[UserChallenge]] = {}

        for challenge in user.challenges:
            all_challenges.setdefault((challenge.level, challenge.name), [])
            all_challenges[(challenge.level, challenge.name)].append(challenge)
        if current_challenge := user.challenge:
            all_challenges.setdefault(
                (current_challenge.level, current_challenge.name), []
            )
            current_challenge.result = "CURRENT"
            all_challenges[(current_challenge.level, current_challenge.name)].append(
                current_challenge
            )

        all_challenges = dict(sorted(all_challenges.items(), key=lambda x: x[0][0]))

        solved = 0
        content = ""
        for challenge_info, challenges in all_challenges.items():
            challenges.sort(key=lambda x: x.attempt)
            content += f"\n{challenge_info[0]} : {challenge_info[1]}\n"
            for challenge in challenges:
                if challenge.result == "OK":
                    solved += 1
                content += f"\t [{challenge.attempt}]  {challenge.result:^9}  {RelativeDateTime(challenge.requested).pretty}\t\n"
        content = f"Total  : {len(all_challenges)}\nSolved : {solved}\n{content}"

        await interaction.followup.send(
            embed=discord.Embed(
                color=self.color.yellow, description=f"```txt\n{content}```"
            )
        )


async def setup(bot):
    await bot.add_cog(Status(bot))
