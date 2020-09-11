import os

from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix='>')

# we dont talk about what is above


@client.event
async def on_ready():
    """runs when bot comes online"""
    print(f"Init as {client.user}")


@client.event
async def on_message(message):
    """an event that happens when any message is sent"""
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )
    if message.author == client.user:
        return

    if "hello" in message.content.lower():
        await message.channel.send('Hi!')

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    """shows the latency between the client and the server in miliseconds"""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.event
async def on_member_join(member):
    """logs a message when a user joins the server"""
    print(f'{member} has joined the server!')


@client.event
async def on_member_remove(member):
    """logs a message when a user leaves the server"""
    print(f'{member} has left the server.')


keep_alive()  # keeps the repl running
client.run(os.environ.get("DISCORD_BOT_SECRET"))
