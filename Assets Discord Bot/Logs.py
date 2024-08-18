import discord
from discord.ext import commands
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_ticket_action(self, log_channel_id, ticket_channel_name, action, user):
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title=f"Ticket {action.capitalize()}",
                description=f"**Ticket:** {ticket_channel_name}\n**Action:** {action.capitalize()}\n**By:** {user.mention}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                color=discord.Color.green() if action == "claimed" else discord.Color.red()
            )
            await log_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logs(bot))
