import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user} is connected')

async def load_cogs():
    for filename in os.listdir('./Assets Discord Bot'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'Assets Discord Bot.{filename[:-3]}')
                print(f'Successfully loaded {filename}')
            except Exception as e:
                print(f'Failed to load {filename}: {e}')

@bot.command(name='reload')
async def reload(ctx, extension):
    try:
        await bot.unload_extension(f'Assets Discord Bot.{extension}')
        await bot.load_extension(f'Assets Discord Bot.{extension}')
        await ctx.send(f'Successfully reloaded {extension}')
    except Exception as e:
        await ctx.send(f'Failed to reload {extension}: {e}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start('YOUR TOKEN')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
