from datetime import UTC, datetime

import discord

from cogs import Cog
from models import Evaluation
from utils import MESSAGE


class Submit(Cog):
    @discord.app_commands.dm_only()
    @discord.app_commands.allowed_installs(guilds=False, users=True)
    @discord.app_commands.command(description="Submit a challenge's code.")
    @discord.app_commands.describe(file="The file to submit.")
    async def submit(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        self.cog_interaction(interaction, file=file)

        if (user := await self.bot.user_is_unkown(interaction)) is None:
            return

        current_challenge = user.challenge
        if current_challenge is None:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=f"{interaction.user.mention}, you don't have any challenge to submit!",
                ).set_footer(text="instead, use /request")
            )
            return

        if current_challenge.submited:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=f"**{current_challenge.name}** {MESSAGE.waiting}",
                ).set_footer(text="be patient!")
            )
            return

        if file.filename != current_challenge.file:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=f"Excepected file **{current_challenge.file}** got **{file.filename}** .",
                ).set_footer(text="strange file!")
            )
            return

        try:
            solution = current_challenge.solution
            await file.save(solution.path)
            if current_challenge.additionales:
                with open(solution.path, "a") as f:
                    print(current_challenge.additionales, file=f)
        except discord.errors.HTTPException or discord.errors.NotFound as e:
            await interaction.followup.send(
                embed=discord.Embed(
                    color=self.color.red,
                    description=f"Failed to read {file.filename} .",
                ).set_footer(text="Suspicious File!")
            )
            print(f"failed to read {file.filename} from {user.name}\nError: {e}")
            return

        user._challenge.update({"submited": str(datetime.now(UTC))})
        Evaluation.create(
            user=user,
            timestamp=current_challenge.timestamp,
            challenge=current_challenge,
        )
        user._log = None
        user.update()

        await interaction.followup.send(
            embed=discord.Embed(
                color=self.color.green,
                description=f"**{current_challenge.name}** {MESSAGE.submiting}",
            ).set_footer(text="Diving into your code!")
        )


async def setup(bot):
    await bot.add_cog(Submit(bot))
