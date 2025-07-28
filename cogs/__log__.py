import discord

from cogs import Cog


class Log(Cog):
    @discord.app_commands.dm_only()
    @discord.app_commands.allowed_installs(guilds=False, users=True)
    @discord.app_commands.command(description="See a failed challenge log.")
    async def log(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.cog_interaction(interaction)

        if (user := await self.bot.user_is_unkown(interaction)) is None:
            return

        user_log = user.log
        if user_log is None:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=f"{interaction.user.mention}, no logs were found.",
                )
            )
            return

        for challenge in user.challenges:
            if challenge.id == user_log.id and challenge.attempt == user_log.attempt:
                user._log = None
                user.update()
                await interaction.followup.send(
                    embed=discord.Embed(
                        color=self.color.orange,
                        title=user_log.name,
                        description=(
                            f"```ansi\n{user_log.trace}```\n"
                            f"**`Result`**: {user_log.result}\n"
                        ),
                    )
                )
                return

        await interaction.followup.send(
            embed=discord.Embed(
                color=self.color.red,
                description=f"{interaction.user.mention}, no logs were found.",
            )
        )


async def setup(bot):
    await bot.add_cog(Log(bot))
