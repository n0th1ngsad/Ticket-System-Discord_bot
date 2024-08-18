import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None
        self.category_id = None
        self.log_channel_id = 1274586141621882881   # CHANGE TO YOUR CHANNEL ID FOR LOGS

    @app_commands.command(name="setup", description="Setup a ticket system with a channel ID and category ID.")
    async def setup(self, interaction: discord.Interaction, channel_id: str, category_id: str):
        try:
            self.channel_id = int(channel_id)
            self.category_id = int(category_id)

            channel = self.bot.get_channel(self.channel_id)
            if not channel:
                await interaction.response.send_message("Invalid channel ID.")
                return

            embed = discord.Embed(
                title="Support Tickets",
                description="Click the button below to create a new support ticket.",
                color=discord.Color.blue()
            )

            button = discord.ui.Button(label="Create Ticket", style=discord.ButtonStyle.green)

            async def button_callback(interaction: discord.Interaction):
                category = self.bot.get_channel(self.category_id)
                if category and isinstance(category, discord.CategoryChannel):
                    ticket_channel = await category.create_text_channel(f'ticket-{interaction.user.name}')
                    
                    admin_role = discord.utils.get(interaction.guild.roles, permissions=discord.Permissions(administrator=True))
                    
                    await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
                    await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
                    if admin_role:
                        await ticket_channel.set_permissions(admin_role, read_messages=True, send_messages=True)
                    
                    close_button = discord.ui.Button(label="Close Ticket", style=discord.ButtonStyle.red)
                    claim_button = discord.ui.Button(label="Claim Ticket", style=discord.ButtonStyle.blurple)

                    async def close_ticket_callback(interaction: discord.Interaction):
                        await self.close_ticket(interaction, ticket_channel, "closed")

                    async def claim_ticket_callback(interaction: discord.Interaction):
                        await self.close_ticket(interaction, ticket_channel, "claimed")

                    close_button.callback = close_ticket_callback
                    claim_button.callback = claim_ticket_callback

                    view = discord.ui.View()
                    view.add_item(claim_button)
                    view.add_item(close_button)

                    await ticket_channel.send(f"{interaction.user.mention} created this ticket.", embed=self.get_ticket_embed(), view=view)
                    await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)
                else:
                    await interaction.response.send_message("Invalid category ID.", ephemeral=True)

            button.callback = button_callback

            view = discord.ui.View()
            view.add_item(button)

            await channel.send(embed=embed, view=view)
            await interaction.response.send_message("Ticket system setup successfully.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    async def close_ticket(self, interaction: discord.Interaction, ticket_channel: discord.TextChannel, action: str):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if not log_channel:
            await interaction.response.send_message("Log channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Ticket {action.capitalize()}",
            description=f"**Ticket:** {ticket_channel.name}\n**Action:** {action.capitalize()}\n**By:** {interaction.user.mention}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=discord.Color.green() if action == "claimed" else discord.Color.red()
        )

        await log_channel.send(embed=embed)
        await ticket_channel.delete(reason=f"Ticket {action.capitalize()} by {interaction.user}")

    def get_ticket_embed(self):
        return discord.Embed(
            title="Ticket Management",
            description="Use the buttons below to manage this ticket.",
            color=discord.Color.blue()
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
