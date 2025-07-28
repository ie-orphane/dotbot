import discord

from cogs import Cog


class Help(Cog):
    @discord.app_commands.dm_only()
    @discord.app_commands.allowed_installs(guilds=False, users=True)
    @discord.app_commands.command(description="Show the challenge's guidlines.")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.cog_interaction(interaction)

        await interaction.followup.send(
            embed=discord.Embed(
                color=self.color.blue,
                description=(
                    "### /request : get a new challenge\n"
                    + "- During the challenge, always follow the **law**  and doubt your code.\n"
                    + "- You have 1 day to submit your code, if you pass the deadline your challenge will be evaluated as `DEAD`.\n"
                    + "### /submit : send your code challenge\n"
                    + "- Your code will be evaluated by a program called **bugini**.\n"
                    + "- You will receive a message with challenge result (`OK` | `ERROR` | `KO` | `FORBIDDEN` | `TIMEOUT`).\n"
                    + "### /status : show your challenge journey\n"
                    + "- see your ancients and current challenges.\n"
                    + "### /log : see the failing part of the last challenge\n"
                    + "- Only the `ERROR` and `KO` challenges will have a log.\n"
                ),
            )
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
