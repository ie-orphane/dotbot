import discord

from cogs import Cog
from utils import MESSAGE


class Request(Cog):
    @discord.app_commands.dm_only()
    @discord.app_commands.allowed_installs(guilds=False, users=True)
    @discord.app_commands.command(description="Request a new challenge.")
    async def request(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.cog_interaction(interaction)

        if (user := await self.bot.user_is_unkown(interaction)) is None:
            return

        current_challenge = user.challenge
        if current_challenge:
            if current_challenge.submited:
                await interaction.followup.send(
                    embed=discord.Embed(
                        color=self.color.red,
                        description=f"**{current_challenge.name}** {MESSAGE.waiting}",
                    ).set_footer(text="be patient!")
                )
                return

            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=(
                        f"### {interaction.user.mention}, you already requested a challenge!\n"
                        f"### {current_challenge.name}\n"
                        f"```ansi\n{current_challenge.subject}```\n"
                        f"**`Level`**: {current_challenge.level}\n"
                        f"**`Excpected File`**: {current_challenge.file}"
                    ),
                )
            )
            return

        challenge = user.request()
        if challenge is None:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.yellow,
                    description=f"### {interaction.user.mention}\n**{MESSAGE.finishing}**",
                )
            )
            return

        await interaction.followup.send(
            embed=discord.Embed(
                color=self.color.yellow,
                title=challenge.name,
                description=(
                    f"```ansi\n{challenge.subject}```\n"
                    f"**`Level`**: {challenge.level}\n"
                    f"**`Excpected File`**: {challenge.file}"
                ),
            ).set_footer(text="as always follow the law and doubt your code!"),
        )


async def setup(bot):
    await bot.add_cog(Request(bot))
