from keep_alive import keep_alive
import os

from discord.ext import commands

client = commands.Bot(command_prefix="?")


### on startup ###
@client.event
async def on_ready():
    print("Init as {0.user}".format(client))


### ping command ###
@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.send(round(latency, 3))


keep_alive()
client.run(os.environ.get("DISCORD_BOT_SECRET"))
