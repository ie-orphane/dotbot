import discord

from cogs import Cog
from models import User


class Create(Cog):
    @discord.app_commands.guild_only()
    @discord.app_commands.allowed_installs(guilds=True, users=False)
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.describe(member="The member to create a profile for.")
    @discord.app_commands.command(description="Create a new member profile.")
    async def create(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        name: str,
    ):
        await interaction.response.defer(ephemeral=True)

        user = User.read(member.id)

        if user:
            await interaction.followup.send(
                embed=discord.Embed(
                    description=f"{member.mention} is already registered.",
                    color=self.color.red,
                ).set_author(name=user.name, icon_url=member.display_avatar.url),
                ephemeral=True,
            )
            return

        user = User.create(name=name, id=member.id)

        await interaction.followup.send(
            embed=discord.Embed(
                description=f"{member.mention} has been successfully registered.",
                color=self.color.green,
            ).set_author(name=user.name, icon_url=member.display_avatar.url),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Create(bot))
